"""Command-line interface to find degrees of separation between two actors."""

import argparse
import csv
import os
import sys
from typing import Dict, List, Optional, Set, Tuple

from util import Node, QueueFrontier

# Global data containers populated by load_data
names: Dict[str, Set[str]] = {}
people: Dict[str, Dict[str, object]] = {}
movies: Dict[str, Dict[str, object]] = {}


def load_data(directory: str) -> None:
    """Load people and movie relationship data from a directory of CSV files.

    Summary:
        Reads people, movies, and stars CSV files into global dictionaries
        for fast lookups during breadth-first search.
    Params:
        directory: Path containing people.csv, movies.csv, and stars.csv.
    Outputs:
        Populates module-level dictionaries `names`, `people`, and `movies`.
    """
    # Load people
    with open(os.path.join(directory, "people.csv"), encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set(),
            }
            key = row["name"].lower()
            if key not in names:
                names[key] = {row["id"]}
            else:
                names[key].add(row["id"])

    # Load movies
    with open(os.path.join(directory, "movies.csv"), encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set(),
            }

    # Load stars
    with open(os.path.join(directory, "stars.csv"), encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                # Skip rows with missing references
                continue


def person_id_for_name(name: str) -> Optional[str]:
    """Resolve a name to a unique person id if possible.

    Summary:
        Handles ambiguous names by prompting the user to select one ID.
    Params:
        name: Name string typed by the user.
    Outputs:
        Returns a person id string or None if no match exists.
    """
    person_ids = list(names.get(name.lower(), set()))
    if not person_ids:
        return None
    if len(person_ids) == 1:
        return person_ids[0]

    # Ambiguity: ask user to choose
    print(f"Which '{name}'?")
    for person_id in person_ids:
        person = people[person_id]
        print(f"ID: {person_id}, Name: {person['name']}, Birth: {person['birth']}")
    try:
        choice = input("Intended Person ID: ")
    except EOFError:
        return None
    return choice if choice in person_ids else None


def neighbors_for_person(person_id: str) -> Set[Tuple[str, str]]:
    """Return (movie_id, person_id) pairs for people who starred together.

    Summary:
        Iterates over every movie the person appeared in and collects
        co-stars associated with that movie.
    Params:
        person_id: ID of the person whose neighbors we want.
    Outputs:
        A set of (movie_id, neighbor_person_id) tuples.
    """
    neighbor_pairs: Set[Tuple[str, str]] = set()
    for movie_id in people[person_id]["movies"]:
        for star_id in movies[movie_id]["stars"]:
            neighbor_pairs.add((movie_id, star_id))
    return neighbor_pairs


def shortest_path(source: str, target: str) -> Optional[List[Tuple[str, str]]]:
    """Use BFS to find the shortest actor/film chain from source to target.

    Summary:
        Expands a breadth-first frontier over the person graph until the
        target actor is found, then reconstructs the path of (movie, person)
        steps from source to target.
    Params:
        source: Person id for the starting actor.
        target: Person id for the destination actor.
    Outputs:
        Ordered list of (movie_id, person_id) tuples representing each step,
        or None if no connection exists.
    """
    start = Node(state=source, parent=None, action=None)
    frontier = QueueFrontier()
    frontier.add(start)
    explored: Set[str] = set()

    while not frontier.empty():
        node = frontier.remove()
        explored.add(node.state)

        for movie_id, person_id in neighbors_for_person(node.state):
            if person_id in explored or frontier.contains_state(person_id):
                continue
            child = Node(state=person_id, parent=node, action=movie_id)
            if person_id == target:
                # Reconstruct path
                chain: List[Tuple[str, str]] = []
                while child.parent is not None:
                    chain.append((child.action, child.state))
                    child = child.parent
                chain.reverse()
                return chain
            frontier.add(child)

    return None


def main() -> None:
    """Interactive CLI for computing degrees of separation."""
    parser = argparse.ArgumentParser(
        description="Find degrees of separation between two actors."
    )
    parser.add_argument(
        "--dataset",
        choices=["small", "large"],
        default="large",
        help="Which dataset folder to load (default: large)",
    )
    args = parser.parse_args()

    data_dir = os.path.join(os.path.dirname(__file__), args.dataset)
    load_data(data_dir)

    print("Data loaded. Nodes: {} people, {} movies".format(len(people), len(movies)))
    source_name = input("Name of source actor: ")
    source_id = person_id_for_name(source_name)
    if source_id is None:
        sys.exit("Source person not found.")

    target_name = input("Name of target actor: ")
    target_id = person_id_for_name(target_name)
    if target_id is None:
        sys.exit("Target person not found.")

    path = shortest_path(source_id, target_id)
    if path is None:
        print("Not connected.")
        return

    print(f"Degrees of separation: {len(path)}")
    current = source_id
    for i, (movie_id, person_id) in enumerate(path, start=1):
        movie = movies[movie_id]["title"]
        actor_from = people[current]["name"]
        actor_to = people[person_id]["name"]
        print(f"{i}: {actor_from} acted with {actor_to} in {movie}")
        current = person_id


if __name__ == "__main__":
    main()
