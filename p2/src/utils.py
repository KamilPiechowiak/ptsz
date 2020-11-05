def lmap(func, iterable):
    return list(map(func, iterable))


def solve_meta(*cls_args):
    class SolveMeta(*cls_args):
        pass

    return SolveMeta
