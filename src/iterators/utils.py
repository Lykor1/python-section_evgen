from dataclasses import dataclass, field
from itertools import batched
from typing import Iterable, TypeAlias

SomeRemoteData: TypeAlias = int


@dataclass
class Query:
    per_page: int = 3
    page: int = 1


@dataclass
class Page:
    per_page: int = 3
    results: Iterable[SomeRemoteData] = field(default_factory=list)
    next: int | None = None


def request(query: Query) -> Page:
    data = [i for i in range(0, 10)]
    chunks = list(batched(data, query.per_page))
    return Page(
        per_page=query.per_page,
        results=chunks[query.page - 1],
        next=query.page + 1 if query.page < len(chunks) else None,
    )


class RetrieveRemoteData:
    def __init__(self, per_page: int = 3):
        self.per_page = per_page

    def __iter__(self):
        page_number = 1
        while True:
            page = request(Query(per_page=self.per_page, page=page_number))
            for obj in page.results:
                yield obj
            if page.next is None:
                break
            page_number = page.next


class Fibo:
    def __init__(self, n: int):
        self.n = n
        self.index = 0
        self.prev = 0
        self.curr = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= self.n:
            raise StopIteration
        if self.index == 0:
            self.index += 1
            return 0
        elif self.index == 1:
            self.index += 1
            return 1
        else:
            value = self.prev + self.curr
            self.prev = self.curr
            self.curr = value
            self.index += 1
            return value
