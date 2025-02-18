from generate_page import static_to_public, generate_pages_recursive

def main():

    from_path = "content"
    dest_path = "public"
    template = "template.html"

    #stat...blic removes /public folder, creates new empty one and copies all from /static to it
    static_to_public()

    #gene...page generates a page based on template file and markdown file
    generate_pages_recursive(from_path, template, dest_path)

main()