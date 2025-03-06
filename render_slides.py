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


# Given a week number and a topic name, renders the 4 slide decks.
def render(week, topic):
    # We have to change into the correct directory for the `marp` command to work properly with
    # the images inside the slides.
    os.chdir(f"week{week}")

    # The default theme in the repository is dark.
    if os.system(f"marp {topic}.md -c ../{MARP_CONFIG} -o {topic}-dark.html") != 0:
        raise Exception(f"Error rendering {topic}-dark.html")

    if os.system(f"marp {topic}.md -c ../{MARP_CONFIG} -o {topic}-dark.pdf") != 0:
        raise Exception(f"Error rendering {topic}-dark.pdf")

    # Render the light theme slides.
    change_theme(f"{topic}.md", light=True)

    if os.system(f"marp {topic}.md -c ../{MARP_CONFIG} -o {topic}-light.html") != 0:
        raise Exception(f"Error rendering {topic}-light.html")

    if os.system(f"marp {topic}.md -c ../{MARP_CONFIG} -o {topic}-light.pdf") != 0:
        raise Exception(f"Error rendering {topic}-light.pdf")

    # Change the theme back to dark.
    change_theme(f"{topic}.md", light=False)

    # Change back to the root directory.
    os.chdir("..")


def main():
    # Create a pool of workers.
    with multiprocessing.Pool(len(TOPICS)) as pool:
        # Create a list of arguments for the render function.
        args = [(week, topic) for week, topic in TOPICS.items()]
        # Use the pool to map the render function to the arguments.
        pool.starmap(render, args)


if __name__ == "__main__":
    main()
