import argparse
import multiprocessing
import os
import signal

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

# Global event to signal workers to stop.
stop_event = multiprocessing.Event()


# Handle SIGINT (Ctrl+C) by setting stop event and terminating the pool.
def signal_handler(sig, frame, pool):
    print("Received Ctrl+C, stopping all rendering...")
    stop_event.set()
    pool.close()
    pool.join()
    print("All workers stopped.")
    exit(1)


# Check if the markdown file has been modified since the outputs were generated.
def needs_rendering(markdown_file, outputs):
    if not all(os.path.exists(out) for out in outputs):
        return True
    md_mtime = os.path.getmtime(markdown_file)
    return any(os.path.getmtime(out) < md_mtime for out in outputs)


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


# Helper function to render the output file while handling interrupts.
def render_output(md_file, out):
    if stop_event.is_set():
        print(f"Interrupted during {out}")
        return False
    if os.system(f"marp {md_file} -c ../{MARP_CONFIG} -o {out}") != 0:
        raise Exception(f"Error rendering {out}")
    return True


# Given a week number and a topic name, renders the 4 slide decks.
def render(week, topic, config):
    week_dir = f"week{week}"
    md_file = f"{topic}.md"

    if stop_event.is_set():
        print(f"Stopping render for {topic} due to interrupt")
        return

    if not os.path.isdir(week_dir) or not os.path.isfile(
        os.path.join(week_dir, md_file)
    ):
        raise FileNotFoundError(f"Missing {week_dir}/{md_file}")

    # We have to change into the correct directory for the `marp` command to work properly with
    # the images inside the slides.
    os.chdir(week_dir)

    # The default theme in the repository is dark.
    if not render_output(md_file, f"{topic}-dark.html"):
        return
    if not render_output(md_file, f"{topic}-dark.pdf"):
        return

    # Render the light theme slides.
    change_theme(f"{md_file}", light=True)
    if not render_output(md_file, f"{topic}-light.html"):
        return
    if not render_output(md_file, f"{topic}-light.pdf"):
        return

    # Change the theme back to dark.
    change_theme(f"{md_file}", light=False)

    # Change back to the root directory.
    os.chdir("..")


def get_render_args(args, parser: argparse.ArgumentParser):
    if args.topics:
        valid_topics = set(TOPICS.values())
        selected_topics = set(args.topics)
        invalid_topics = selected_topics - valid_topics

        if invalid_topics:
            parser.error(f"Invalid topics specified: {invalid_topics}")

        topics = {
            week: topic for week, topic in TOPICS.items() if topic in selected_topics
        }
    elif args.modified:
        # Filter topics based on modification status.
        topics = dict()
        for week, topic in TOPICS.items():
            week_dir = f"week{week}"
            md_file = f"{topic}.md"
            outputs = [
                f"{topic}-dark.html",
                f"{topic}-dark.pdf",
                f"{topic}-light.html",
                f"{topic}-light.pdf",
            ]
            if needs_rendering(os.path.join(week_dir, md_file), outputs):
                topics[week] = topic
            else:
                print(f"Skipping {topic} in week {week}: outputs are up-to-date")
    else:
        topics = TOPICS

    return [(week, topic, args.config) for week, topic in topics.items()]


# Parse the command-line arguments.
def parse_args(parser: argparse.ArgumentParser):
    parser.add_argument("--config", default=MARP_CONFIG, help="Marp config file")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--force", action="store_true", help="Force render all slides")
    group.add_argument(
        "--modified", action="store_true", help="Render only modified slides"
    )
    group.add_argument(
        "--topics",
        nargs="+",
        help="Render specific topics by name (e.g., introduction ownership_p1)",
    )

    return parser.parse_args()


def main():
    parser = argparse.ArgumentParser(description="Render Marp slides for a Rust course")
    args = parse_args(parser)

    with multiprocessing.Pool(min(len(TOPICS), multiprocessing.cpu_count())) as pool:
        render_args = get_render_args(args, parser)
        results = pool.starmap_async(render, render_args)

        # Signal handler for Ctrl+C.
        signal.signal(
            signal.SIGINT, lambda sig, frame: signal_handler(sig, frame, pool)
        )

        try:
            results.wait()
            if not results.successful():
                print("Some rendering tasks failed")
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
        finally:
            pool.close()
            pool.join()


if __name__ == "__main__":
    main()
