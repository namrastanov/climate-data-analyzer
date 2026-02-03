"""Parallel processing utilities."""

import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Callable, Iterator, List, TypeVar, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

T = TypeVar("T")
R = TypeVar("R")


@dataclass
class TaskResult:
    """Result of a parallel task."""
    index: int
    success: bool
    result: any = None
    error: str = None


def get_optimal_workers() -> int:
    """Get optimal number of worker processes."""
    cpu_count = os.cpu_count() or 4
    return min(cpu_count, 16)


def parallel_map(
    func: Callable[[T], R],
    items: List[T],
    max_workers: Optional[int] = None,
    chunk_size: int = 1
) -> List[TaskResult]:
    """Apply function to items in parallel."""
    max_workers = max_workers or get_optimal_workers()
    results = []
    
    logger.info(f"Starting parallel processing with {max_workers} workers")
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(func, item): i
            for i, item in enumerate(items)
        }
        
        for future in as_completed(futures):
            idx = futures[future]
            try:
                result = future.result()
                results.append(TaskResult(idx, True, result))
            except Exception as e:
                logger.error(f"Task {idx} failed: {e}")
                results.append(TaskResult(idx, False, error=str(e)))
    
    results.sort(key=lambda x: x.index)
    return results


def chunked_parallel_map(
    func: Callable[[List[T]], List[R]],
    items: List[T],
    chunk_size: int = 1000,
    max_workers: Optional[int] = None
) -> List[R]:
    """Process items in chunks with parallel execution."""
    chunks = [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]
    
    results = parallel_map(func, chunks, max_workers)
    
    all_results = []
    for task_result in results:
        if task_result.success:
            all_results.extend(task_result.result)
    
    return all_results


class ProgressTracker:
    """Track progress of parallel tasks."""

    def __init__(self, total: int):
        self.total = total
        self.completed = 0
        self.failed = 0

    def update(self, success: bool = True) -> None:
        """Update progress."""
        self.completed += 1
        if not success:
            self.failed += 1

    @property
    def progress(self) -> float:
        """Get progress percentage."""
        return (self.completed / self.total) * 100 if self.total > 0 else 0

    def __str__(self) -> str:
        return f"Progress: {self.completed}/{self.total} ({self.progress:.1f}%)"
