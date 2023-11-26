from __future__ import annotations
import json
import math
from typing import List

# Datum class.
# DO NOT MODIFY.


class Datum():
    def __init__(self,
                 coords: tuple[int],
                 code: str):
        self.coords = coords
        self.code = code

    def to_json(self) -> str:
        dict_repr = {'code': self.code, 'coords': self.coords}
        return (dict_repr)

# Internal node class.
# DO NOT MODIFY.


class NodeInternal():
    def __init__(self,
                 splitindex: int,
                 splitvalue: float,
                 leftchild,
                 rightchild):
        self.splitindex = splitindex
        self.splitvalue = splitvalue
        self.leftchild = leftchild
        self.rightchild = rightchild

# Leaf node class.
# DO NOT MODIFY.


class NodeLeaf():
    def __init__(self,
                 data: List[Datum]):
        self.data = data

# KD tree class.


class KDtree():
    def __init__(self,
                 k: int,
                 m: int,
                 root=None):
        self.k = k
        self.m = m
        self.root = root

    # For the tree rooted at root, dump the tree to stringified JSON object and return.
    # DO NOT MODIFY.
    def dump(self) -> str:
        def _to_dict(node) -> dict:
            if isinstance(node, NodeLeaf):
                return {
                    "p": str([{'coords': datum.coords, 'code': datum.code} for datum in node.data])
                }
            else:
                return {
                    "splitindex": node.splitindex,
                    "splitvalue": node.splitvalue,
                    "l": (_to_dict(node.leftchild) if node.leftchild is not None else None),
                    "r": (_to_dict(node.rightchild) if node.rightchild is not None else None)
                }
        if self.root is None:
            dict_repr = {}
        else:
            dict_repr = _to_dict(self.root)
        return json.dumps(dict_repr, indent=2)

    # Insert the Datum with the given code and coords into the tree.
    # The Datum with the given coords is guaranteed to not be in the tree.
    def insert(self, point: tuple[int], code: str):
        if not self.root:
            # root is empty
            self.root = NodeLeaf([Datum(point, code)])
            return
        # navigate to leaf
        parent = None
        current = self.root
        while not isinstance(current, NodeLeaf):
            parent = current
            splitindex = current.splitindex
            splitvalue = current.splitvalue
            if point[splitindex] >= splitvalue:
                current = current.rightchild
            else:
                current = current.leftchild
        current.data.append(Datum(point, code))
        if len(current.data) > self.m:
            # split
            # find coord with
            spreads = []
            for i in range(self.k):
                values = [datum.coords[i] for datum in current.data]
                spread = max(values) - min(values)
                spreads.append((i, spread))
            spreads.sort(key=lambda x: (-x[1], x[0]))
            splitindex = spreads[0][0]
            current.data.sort(
                key=lambda lst: [lst.coords[i] for i, _ in spreads])
            mid = (self.m+1) // 2
            left = current.data[:mid]
            right = current.data[mid:]
            if len(current.data) % 2 == 1:
                splitvalue = float(current.data[mid].coords[splitindex])
            else:
                splitvalue = float((
                    current.data[mid-1].coords[splitindex] + current.data[mid].coords[splitindex]) / 2)
            split = NodeInternal(splitindex, splitvalue,
                                 NodeLeaf(left), NodeLeaf(right))
            if not parent:
                self.root = split
                return
            if parent.leftchild == current:
                parent.leftchild = split
                return
            parent.rightchild = split

    # Delete the Datum with the given point from the tree.
    # The Datum with the given point is guaranteed to be in the tree.

    def delete(self, point: tuple[int]):
        thisisaplaceholder = True

    # Find the k nearest neighbors to the point.
    def knn(self, k: int, point: tuple[int]) -> str:
        # Use the strategy discussed in class and in the notes.
        # The list should be a list of elements of type Datum.
        # While recursing, count the number of leaf nodes visited while you construct the list.
        # The following lines should be replaced by code that does the job.
        leaveschecked = 0
        knnlist = []
        # The following return line can probably be left alone unless you make changes in variable names.
        return (json.dumps({"leaveschecked": leaveschecked, "points": [datum.to_json() for datum in knnlist]}, indent=2))
