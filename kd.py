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
        gramp = None
        parent = None
        current = self.root
        while not isinstance(current, NodeLeaf):
            gramp = parent
            parent = current
            splitindex = current.splitindex
            splitvalue = current.splitvalue
            if point[splitindex] >= splitvalue:
                current = current.rightchild
            else:
                current = current.leftchild
        index = 0
        for i, datum in enumerate(current.data):
            if datum.coords == point:
                index = i
                break
        current.data.pop(index)
        if len(current.data) > 0:
            return
        if not parent:
            self.root = None
            return
        if not gramp:
            if current == parent.leftchild:
                self.root = parent.rightchild
            else:
                self.root = parent.leftchild
            return
        if gramp.leftchild == parent:
            if current == parent.leftchild:
                gramp.leftchild = parent.rightchild
            else:
                gramp.leftchild = parent.leftchild
        else:
            if current == parent.leftchild:
                gramp.rightchild = parent.rightchild
            else:
                gramp.rightchild = parent.leftchild

    # Find the k nearest neighbors to the point.

    def knn(self, k: int, point: tuple[int]) -> str:
        # Use the strategy discussed in class and in the notes.
        # The list should be a list of elements of type Datum.
        # While recursing, count the number of leaf nodes visited while you construct the list.
        # The following lines should be replaced by code that does the job.
        knnlist = []
        leaveschecked = 0

        def getboundingbox(node, box):
            if not node:
                return
            if isinstance(node, NodeLeaf):
                for point in node.data:
                    for i in range(self.k):
                        box[i][0] = min(box[i][0], point.coords[i])
                        box[i][1] = max(box[i][1], point.coords[i])
            else:
                getboundingbox(node.leftchild, box)
                getboundingbox(node.rightchild, box)

        def distancepoints(point1, point2):
            if isinstance(point1, Datum):
                point1 = point1.coords
            if isinstance(point2, Datum):
                point2 = point2.coords
            val = 0
            for i in range(self.k):
                val += (point1[i] - point2[i]) ** 2
            return val

        def distancebox(point, box):
            if isinstance(point, Datum):
                point = point.coords
            val = 0
            for i in range(self.k):
                if point[i] < box[i][0]:
                    val += (box[i][0]-point[i]) ** 2
                elif point[i] > box[i][1]:
                    val += (point[i]-box[i][1]) ** 2
            return val

        def knnh(node):
            if isinstance(node, NodeInternal):
                leftbox = [[float('inf'), float('-inf')]
                           for _ in range(self.k)]
                rightbox = [[float('inf'), float('-inf')]
                            for _ in range(self.k)]
                getboundingbox(node.leftchild, leftbox)
                getboundingbox(node.rightchild, rightbox)
                leftdistance = rightdistance = -1
                maxdistance = float('inf')
                if knnlist:
                    maxdistance = distancepoints(
                        point, knnlist[-1])
                if node.leftchild:
                    leftdistance = distancebox(point, leftbox)
                if node.rightchild:
                    rightdistance = distancebox(point, rightbox)
                # choosing paths
                leaves = 0
                if rightdistance == -1 and (len(knnlist) < k or leftdistance <= maxdistance):
                    # left is only option and could improve list
                    leaves += knnh(node.leftchild)
                elif leftdistance == -1 and (len(knnlist) < k or rightdistance <= maxdistance):
                    # right is the only option and could improve list
                    leaves += knnh(node.rightchild)
                elif leftdistance <= rightdistance and (len(knnlist) < k or leftdistance <= maxdistance):
                    # left is preferred
                    leaves += knnh(node.leftchild)
                    # check if it makes sense to go right
                    maxdistance = distancepoints(
                        point, knnlist[-1])
                    if len(knnlist) < k or rightdistance <= maxdistance:
                        leaves += knnh(node.rightchild)
                elif rightdistance < leftdistance and (len(knnlist) < k or rightdistance <= maxdistance):
                    # right is preferred
                    leaves += knnh(node.rightchild)
                    # check if it makes sense to go left
                    maxdistance = distancepoints(
                        point, knnlist[-1])
                    if len(knnlist) < k or leftdistance <= maxdistance:
                        leaves += knnh(node.leftchild)
                return leaves
            else:
                # at a leaf
                for datum in node.data:
                    if len(knnlist) < k:
                        knnlist.append(datum)
                        knnlist.sort(key=lambda datum: (
                            distancepoints(datum, point), datum.code))
                    else:
                        for i in range(k):
                            comp = knnlist[i]
                            if distancepoints(datum, point) < distancepoints(comp, point) or (distancepoints(datum, point) == distancepoints(comp, point) and datum.code < comp.code):
                                knnlist.insert(i, datum)
                                knnlist.pop()
                                break
                return 1

        leaveschecked = knnh(self.root)

        # The following return line can probably be left alone unless you make changes in variable names.
        return (json.dumps({"leaveschecked": leaveschecked, "points": [datum.to_json() for datum in knnlist]}, indent=2))
