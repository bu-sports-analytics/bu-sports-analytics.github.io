import argparse
from bs4 import BeautifulSoup, Comment
import os

def clean_mailchimp_html(html_string):
    """
    Cleans Mailchimp newsletter HTML by removing boilerplate and extracting
    the main content, formatted similar to Version 1.

    Args:
        html_string: A string containing the raw HTML of the Mailchimp archive page (Version 2 type).

    Returns:
        A string containing the markdown frontmatter and cleaned HTML body fragment,
        or None if crucial elements are not found.
    """
    try:
        # Parse the full HTML initially to find elements like title and excerpt
        soup = BeautifulSoup(html_string, 'html.parser')

        # --- 1. Extract Title and Excerpt for Frontmatter ---
        # Find a suitable title source (prioritize og:title, then <title>)
        title = "Newsletter Title" # Default title
        og_title_meta = soup.find('meta', property='og:title')
        if og_title_meta and og_title_meta.get('content'):
             title = og_title_meta['content'].strip()
        else:
             title_tag = soup.find('title')
             if title_tag and title_tag.string:
                  title = title_tag.string.strip()

        # Find the first h1 element for the excerpt, as requested
        first_h1 = soup.find('h1')
        excerpt = first_h1.get_text(strip=True) if first_h1 else "Default excerpt"

        # --- 2. Prepare for Cleaning the Body Content ---
        # Find the main body tag to perform cleaning within its subtree
        body_tag = soup.find('body')
        if not body_tag:
             print("Error: Could not find the <body> tag in the input HTML.")
             return None

        # --- 3. Remove Boilerplate Elements from the Body's Content ---

        # Remove the Mailchimp archive bar wrapper if it exists within the body
        archive_wrap = body_tag.find(id='awesomewrap')
        if archive_wrap:
            archive_wrap.extract()

        # Remove script tags within the body (if any were left after head removal)
        for script in body_tag.find_all('script'):
            script.extract()

        # Remove specific hidden divs/spans if they are inside the body
        preview_text = body_tag.find('span', class_='mcnPreviewText')
        if preview_text:
             preview_text.extract()
        # This style is quite specific to Mailchimp filler content
        hidden_div = body_tag.find('div', style="display: none; max-height: 0px; overflow: hidden;")
        if hidden_div:
             hidden_div.extract()

        # Remove comments within the body tag (optional, but cleans up)
        for comment in body_tag.find_all(string=lambda text: isinstance(text, Comment)):
             comment.extract()

        # --- 4. Remove the Footer Section based on class markers ---

        # Find the main content table within the body
        body_table = body_tag.find('table', id='bodyTable')
        # print(body_table) # this part is good

        if not body_table:
            print("Error: Could not find the main table with id='bodyTable'.")
            return None

        # Find the root table within the body cell (this contains the actual email content sections)
        root_table = body_table.find('table', id='root')

        if not root_table:
             print("Error: Could not find the root table with id='root' within bodyTable.")
             return None

        # Find the main tbody directly inside root_table (it holds the section wrappers)
        root_tbody_count = 0
        for root_tbody in root_table.find_all('tbody', recursive=False):
            root_tbody_count += 1
            print(root_tbody_count)
            if root_tbody:
                # print(root_tbody) # Debugging
                # Look for tbody.mceWrapper children that specifically contain a td.mceSectionFooter
                footer_wrapper = None
                # for wrapper_tbody in root_tbody.find_all('tbody', class_='mceWrapper', recursive=False):
                    # print(f'wrapper_tbody: {wrapper_tbody}')
                    # Look for a <td class="mceSectionFooter"> inside a <tr> inside this tbody
                found_footer_td = root_tbody.find('tr')
                # print(f'tr: {found_footer_td}') # Debugging
                if found_footer_td:
                    footer_td = found_footer_td.find('td', class_='mceSectionFooter')
                    footer_section = found_footer_td.find('td', class_='mceFooterSection')
                    # print(f'td: {footer_td}, footer_section: {footer_section}')
                    if footer_td or footer_section:
                        # print(f"Found footer wrapper with data-block-id: {root_tbody.get('data-block-id')}") # Debugging
                        footer_wrapper = root_tbody
                        # break # Assuming there's only one footer section                                                                             
                    if footer_wrapper:
                        # print("hey")
                        # print(f"Found footer wrapper with data-block-id: {footer_wrapper.get('data-block-id')}") # Debugging
                        footer_wrapper.extract() # Remove the entire footer tbody from the tree
                        # print("Successfully extracted footer wrapper.") # Debug
                    else:
                        print("Warning: Could not find the footer wrapper (tbody.mceWrapper containing td.mceSectionFooter) within #root's primary tbody.")
            else:
                print("Warning: Could not find the primary tbody directly inside #root table.")
        for social_media in root_table.find_all('td', class_="mceSocialFollowIcon"):
            print(social_media)
            social_media.extract()
        # Delete link to view email inside browser
        view_email = body_tag.find('a', text="View this email in your browser")
        if view_email:
            view_email.extract()
        second_view_email = body_tag.find('a', text="View email in browser")
        if second_view_email:
            second_view_email.extract()

        # --- 5. Reconstruct the Output HTML ---
        # The goal is to get the content starting from the <center> tag inside the original body
        # Find the <center> tag again within the (now cleaned) original body_tag object
        cleaned_center_tag = body_tag.find('center')

        if not cleaned_center_tag:
             print("Error: Could not find the <center> tag in the cleaned body contents.")
             return None

        # Get the string representation of the cleaned center tag and its contents
        # Using .prettify() can help with indentation, but might add extra newlines.
        # Using str() preserves more of the original formatting, but might be less readable.
        # Let's stick to str() for closer resemblance to Version 1 structure.
        cleaned_center_string = str(cleaned_center_tag)


        # Combine frontmatter and the new body tag with the cleaned content
        new_title = title.replace('"', '\\"') # Escape double quotes for YAML
        new_excerpt = excerpt.replace('"', '\\"') # Escape double quotes for YAML
        output_html = f"""---
title: "{new_title}"
excerpt: "{new_excerpt}"
---
    {cleaned_center_string}
""" # Added indentation for the center tag within body as per Version 1

        return output_html

    except Exception as e:
        print(f"An error occurred during cleaning: {e}")
        import traceback
        # print(f"Traceback: {traceback.format_exc()}") # Optional: for more detailed errors
        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean Mailchimp newsletter HTML.")
    parser.add_argument("input_file", help="Path to the input Mailchimp HTML file (Version 2 type).")
    parser.add_argument("output_file", help="Path to the output cleaned HTML file (Version 1 type).")

    args = parser.parse_args()

    # Read the input file
    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"Error: Input file not found at {args.input_file}")
        exit(1)
    except Exception as e:
        print(f"Error reading input file {args.input_file}: {e}")
        exit(1)

    # Clean the HTML
    print(f"Cleaning HTML from {args.input_file}...")
    cleaned_html = clean_mailchimp_html(html_content)

    if cleaned_html is None:
        print("Cleaning process failed. Output file not created.")
        exit(1)

    # Write the output file
    try:
        with open(args.output_file, 'w', encoding='utf-8') as f:
            f.write(cleaned_html)
        print(f"Successfully cleaned HTML written to {args.output_file}")
    except Exception as e:
        print(f"Error writing output file {args.output_file}: {e}")
        exit(1)