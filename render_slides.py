import argparse
import multiprocessing
import os

# The configuration file.
MARP_CONFIG = "marp_config.json"

# The topics for each week.
TOPICS = {
    1: "introduction",
    2: "ownership_p1",
    3: "structs_enums",
    4: "collections_generics",
    5: "errors_traits",
    6: "modules_testing",
    7: "closures_iterators",
    8: "ownership_p2",
    9: "lifetimes",
    10: "smart_pointers",
    11: "unsafe",
    12: "parallelism",
    13: "concurrency",
}


# Given a filename, changes the Marp theme.
def change_theme(filename, light):
    f = open(filename, "r")
    filedata = f.read()
    f.close()

    if light:
        newdata = filedata.replace("class: invert", "# class: invert")
    else:
        newdata = filedata.replace("# class: invert", "class: invert")

    f = open(filename, "w")
    f.write(newdata)
    f.close()

# Check if the md file has been modified since the outputs were generated
def needs_rendering(md_file, outputs):
    if not all(os.path.exists(out) for out in outputs):
        return True
    md_mtime = os.path.getmtime(md_file)
    return any(os.path.getmtime(out) < md_mtime for out in outputs)


# Given a week number and a topic name, renders the 4 slide decks.
def render(week, topic, config):
    week_dir = f"week{week}"
    md_file = f"{topic}.md"

    if not os.path.isdir(week_dir) or not os.path.isfile(os.path.join(week_dir, md_file)):
        raise FileNotFoundError(f"Missing {week_dir}/{md_file}")
    
    outputs = [
        f"{topic}-dark.html",
        f"{topic}-dark.pdf",
        f"{topic}-light.html",
        f"{topic}-light.pdf"
    ]
    
    # We have to change into the correct directory for the `marp` command to work properly with
    # the images inside the slides.
    os.chdir(week_dir)

    # The default theme in the repository is dark.
    if os.system(f"marp {md_file} -c ../{MARP_CONFIG} -o {topic}-dark.html") != 0:
        raise Exception(f"Error rendering {topic}-dark.html")

    if os.system(f"marp {md_file} -c ../{MARP_CONFIG} -o {topic}-dark.pdf") != 0:
        raise Exception(f"Error rendering {topic}-dark.pdf")

    # Render the light theme slides.
    change_theme(f"{md_file}", light=True)

    if os.system(f"marp {md_file} -c ../{MARP_CONFIG} -o {topic}-light.html") != 0:
        raise Exception(f"Error rendering {topic}-light.html")

    if os.system(f"marp {md_file} -c ../{MARP_CONFIG} -o {topic}-light.pdf") != 0:
        raise Exception(f"Error rendering {topic}-light.pdf")

    # Change the theme back to dark.
    change_theme(f"{md_file}", light=False)

    # Change back to the root directory.
    os.chdir("..")


def parse_args(parser: argparse.ArgumentParser):
    parser.add_argument("--config", default=MARP_CONFIG, help="Marp config file")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--force", action="store_true", help="Force render all slides")
    group.add_argument("--modified", action="store_true", help="Render only modified slides")
    group.add_argument("--topics", nargs="+", help="Render specific topics by name (e.g., introduction ownership_p1)")
    
    return parser.parse_args()

def get_render_args(args, parser: argparse.ArgumentParser):
    if args.topics:
        valid_topics = set(TOPICS.values())
        selected_topics = set(args.topics)
        invalid_topics = selected_topics - valid_topics
        if invalid_topics:
            parser.error(f"Invalid topics specified: {invalid_topics}")
        topics = {week: topic for week, topic in TOPICS.items() if topic in selected_topics}
    elif args.modified:
        # Filter topics based on modification status
        topics = {}
        for week, topic in TOPICS.items():
            week_dir = f"week{week}"
            md_file = f"{topic}.md"
            outputs = [
                f"{topic}-dark.html",
                f"{topic}-dark.pdf",
                f"{topic}-light.html",
                f"{topic}-light.pdf"
            ]
            if needs_rendering(os.path.join(week_dir, md_file), outputs):
                topics[week] = topic
            else:
                print(f"Skipping {topic} in week {week}: outputs are up-to-date")
    else:
        topics = TOPICS

    return [(week, topic, args.config) for week, topic in topics.items()]

def main():
    parser = argparse.ArgumentParser(description="Render Marp slides for a Rust course")
    args = parse_args(parser)

    with multiprocessing.Pool(min(len(TOPICS), multiprocessing.cpu_count())) as pool:
        render_args = get_render_args(args, parser)
        pool.starmap(render, render_args)


if __name__ == "__main__":
    main()
