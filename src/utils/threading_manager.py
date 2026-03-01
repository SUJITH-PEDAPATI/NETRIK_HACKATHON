"""
Threading & Concurrency Manager for HR Automation System
Provides thread pool management, concurrent processing, and async operations
"""

import threading
import queue
import logging
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed, wait
from typing import Callable, List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import functools


class ProcessingMode(Enum):
    """Processing mode selection"""
    SEQUENTIAL = "sequential"       # Single-threaded (default)
    THREADED = "threaded"           # Multi-threaded (I/O bound)
    PROCESS = "process"             # Multi-process (CPU bound)


@dataclass
class ThreadPoolConfig:
    """Configuration for thread pools"""
    max_workers: int = 4                        # Number of worker threads
    queue_size: int = 1000                      # Queue max size
    timeout: float = 30.0                       # Task timeout in seconds
    enable_monitoring: bool = True              # Monitor thread health
    batch_size: int = 10                        # Items per batch


@dataclass
class TaskResult:
    """Result of a concurrent task"""
    task_id: str
    success: bool
    result: Any = None
    error: Optional[str] = None
    duration_ms: float = 0.0
    thread_id: int = field(default_factory=threading.get_ident)
    timestamp: float = field(default_factory=time.time)


class ThreadSafeLogger:
    """Thread-safe logging wrapper"""
    
    def __init__(self, logger_name: str):
        self.logger = logging.getLogger(logger_name)
        self._lock = threading.RLock()
    
    def log(self, level: int, message: str, extra: Optional[Dict] = None):
        """Thread-safe logging"""
        with self._lock:
            if extra:
                self.logger.log(level, message, extra=extra)
            else:
                self.logger.log(level, message)
    
    def info(self, message: str):
        self.log(logging.INFO, message)
    
    def error(self, message: str):
        self.log(logging.ERROR, message)
    
    def warning(self, message: str):
        self.log(logging.WARNING, message)
    
    def debug(self, message: str):
        self.log(logging.DEBUG, message)


class ConcurrentBatchProcessor:
    """
    High-performance batch processor with thread pooling
    
    Example:
        processor = ConcurrentBatchProcessor(
            max_workers=8,
            batch_size=50
        )
        results = processor.process_batch(
            items=candidates,
            task_fn=evaluate_candidate,
            mode=ProcessingMode.THREADED
        )
    """
    
    def __init__(
        self,
        max_workers: int = 4,
        batch_size: int = 10,
        enable_monitoring: bool = True,
        name: str = "BatchProcessor"
    ):
        self.max_workers = max_workers
        self.batch_size = batch_size
        self.enable_monitoring = enable_monitoring
        self.name = name
        
        self.logger = ThreadSafeLogger(f"{self.name}")
        self._results = []
        self._processing_lock = threading.RLock()
        self._completed_count = 0
        self._failed_count = 0
        self._start_time = None
    
    def process_batch(
        self,
        items: List[Any],
        task_fn: Callable,
        mode: ProcessingMode = ProcessingMode.THREADED,
        **kwargs
    ) -> List[TaskResult]:
        """
        Process items concurrently
        
        Args:
            items: List of items to process
            task_fn: Function to apply (must be picklable for PROCESS mode)
            mode: Sequential, threaded, or process-based
            **kwargs: Additional args passed to task_fn
        
        Returns:
            List of TaskResult objects
        """
        if mode == ProcessingMode.SEQUENTIAL:
            return self._process_sequential(items, task_fn, **kwargs)
        elif mode == ProcessingMode.THREADED:
            return self._process_threaded(items, task_fn, **kwargs)
        elif mode == ProcessingMode.PROCESS:
            return self._process_multiprocess(items, task_fn, **kwargs)
    
    def _process_sequential(
        self,
        items: List[Any],
        task_fn: Callable,
        **kwargs
    ) -> List[TaskResult]:
        """Sequential processing (baseline)"""
        self.logger.info(f"Processing {len(items)} items sequentially")
        results = []
        
        for idx, item in enumerate(items):
            try:
                start = time.time()
                result = task_fn(item, **kwargs)
                duration = (time.time() - start) * 1000
                
                results.append(TaskResult(
                    task_id=f"task_{idx}",
                    success=True,
                    result=result,
                    duration_ms=duration
                ))
            except Exception as e:
                results.append(TaskResult(
                    task_id=f"task_{idx}",
                    success=False,
                    error=str(e),
                    duration_ms=0
                ))
        
        return results
    
    def _process_threaded(
        self,
        items: List[Any],
        task_fn: Callable,
        **kwargs
    ) -> List[TaskResult]:
        """Multi-threaded processing (I/O bound)"""
        self.logger.info(
            f"Processing {len(items)} items with {self.max_workers} threads"
        )
        self._start_time = time.time()
        self._results = [None] * len(items)
        self._completed_count = 0
        self._failed_count = 0
        
        with ThreadPoolExecutor(max_workers=self.max_workers, thread_name_prefix=self.name) as executor:
            # Submit all tasks
            future_to_idx = {
                executor.submit(self._safe_task_wrapper, task_fn, item, idx, **kwargs): idx
                for idx, item in enumerate(items)
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_idx):
                idx = future_to_idx[future]
                try:
                    task_result = future.result(timeout=30)
                    self._results[idx] = task_result
                    self._completed_count += 1
                except Exception as e:
                    self._results[idx] = TaskResult(
                        task_id=f"task_{idx}",
                        success=False,
                        error=f"Task failed: {str(e)}",
                        duration_ms=0
                    )
                    self._failed_count += 1
        
        elapsed = (time.time() - self._start_time) * 1000
        self.logger.info(
            f"Batch complete: {self._completed_count} succeeded, "
            f"{self._failed_count} failed in {elapsed:.0f}ms"
        )
        
        return self._results
    
    def _process_multiprocess(
        self,
        items: List[Any],
        task_fn: Callable,
        **kwargs
    ) -> List[TaskResult]:
        """Multi-process processing (CPU bound)"""
        self.logger.info(
            f"Processing {len(items)} items with {self.max_workers} processes"
        )
        self._start_time = time.time()
        self._results = [None] * len(items)
        self._completed_count = 0
        self._failed_count = 0
        
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_idx = {
                executor.submit(self._safe_task_wrapper, task_fn, item, idx, **kwargs): idx
                for idx, item in enumerate(items)
            }
            
            for future in as_completed(future_to_idx):
                idx = future_to_idx[future]
                try:
                    task_result = future.result(timeout=30)
                    self._results[idx] = task_result
                    self._completed_count += 1
                except Exception as e:
                    self._results[idx] = TaskResult(
                        task_id=f"task_{idx}",
                        success=False,
                        error=f"Process task failed: {str(e)}",
                        duration_ms=0
                    )
                    self._failed_count += 1
        
        elapsed = (time.time() - self._start_time) * 1000
        self.logger.info(
            f"Multi-process batch complete: {self._completed_count} succeeded, "
            f"{self._failed_count} failed in {elapsed:.0f}ms"
        )
        
        return self._results
    
    @staticmethod
    def _safe_task_wrapper(
        task_fn: Callable,
        item: Any,
        task_idx: int,
        **kwargs
    ) -> TaskResult:
        """Safely execute task with timing and error handling"""
        start = time.time()
        try:
            result = task_fn(item, **kwargs)
            duration = (time.time() - start) * 1000
            
            return TaskResult(
                task_id=f"task_{task_idx}",
                success=True,
                result=result,
                duration_ms=duration
            )
        except Exception as e:
            duration = (time.time() - start) * 1000
            return TaskResult(
                task_id=f"task_{task_idx}",
                success=False,
                error=str(e),
                duration_ms=duration
            )
    
    def get_stats(self) -> Dict[str, Any]:
        """Get processing statistics"""
        if not self._start_time:
            return {}
        
        total_time = time.time() - self._start_time
        total_duration = sum(r.duration_ms for r in self._results if r) / 1000
        
        return {
            "total_time_seconds": total_time,
            "total_item_processing_seconds": total_duration,
            "efficiency_ratio": total_duration / total_time if total_time > 0 else 0,
            "completed": self._completed_count,
            "failed": self._failed_count,
            "total": len(self._results),
            "success_rate": (
                self._completed_count / len(self._results)
                if len(self._results) > 0 else 0
            )
        }


class AsyncAuditLogger:
    """
    Asynchronous audit logging using producer-consumer pattern
    Prevents logging from blocking main thread
    """
    
    def __init__(self, base_logger_name: str = "AuditLog"):
        self.logger = logging.getLogger(base_logger_name)
        self._queue: queue.Queue = queue.Queue(maxsize=10000)
        self._worker_thread = threading.Thread(
            target=self._log_worker,
            daemon=True,
            name="AuditLogWorker"
        )
        self._stop_event = threading.Event()
        self._worker_thread.start()
    
    def log_event(
        self,
        event_type: str,
        data: Dict[str, Any],
        level: int = logging.INFO
    ) -> bool:
        """
        Queue a log event (non-blocking)
        
        Args:
            event_type: Type of event
            data: Event data
            level: Log level
        
        Returns:
            True if queued, False if queue full
        """
        try:
            self._queue.put_nowait((event_type, data, level))
            return True
        except queue.Full:
            self.logger.warning("Audit log queue full, dropping event")
            return False
    
    def _log_worker(self):
        """Worker thread that consumes log events"""
        while not self._stop_event.is_set():
            try:
                event_type, data, level = self._queue.get(timeout=1.0)
                self.logger.log(
                    level,
                    f"[{event_type}] {data}"
                )
            except queue.Empty:
                continue
            except Exception as e:
                self.logger.error(f"Error in audit log worker: {e}")
    
    def flush(self):
        """Wait for all queued events to be logged"""
        self._queue.join()
    
    def shutdown(self):
        """Shutdown the async logger gracefully"""
        self.flush()
        self._stop_event.set()
        self._worker_thread.join(timeout=5.0)


class WorkerPool:
    """
    Generic worker pool for long-running background tasks
    """
    
    def __init__(self, num_workers: int = 4, name: str = "WorkerPool"):
        self.num_workers = num_workers
        self.name = name
        self.logger = ThreadSafeLogger(name)
        self.executor = ThreadPoolExecutor(
            max_workers=num_workers,
            thread_name_prefix=name
        )
        self._pending_futures = {}
        self._lock = threading.Lock()
    
    def submit_task(
        self,
        task_fn: Callable,
        task_id: str,
        *args,
        **kwargs
    ) -> str:
        """Submit a task to the worker pool"""
        future = self.executor.submit(task_fn, *args, **kwargs)
        
        with self._lock:
            self._pending_futures[task_id] = future
        
        self.logger.info(f"Task {task_id} submitted")
        return task_id
    
    def get_result(self, task_id: str, timeout: Optional[float] = None) -> Any:
        """Get result of a submitted task"""
        with self._lock:
            if task_id not in self._pending_futures:
                raise ValueError(f"Task {task_id} not found")
            future = self._pending_futures[task_id]
        
        result = future.result(timeout=timeout)
        
        with self._lock:
            del self._pending_futures[task_id]
        
        return result
    
    def is_done(self, task_id: str) -> bool:
        """Check if task is complete"""
        with self._lock:
            if task_id not in self._pending_futures:
                return False
            return self._pending_futures[task_id].done()
    
    def shutdown(self, wait: bool = True):
        """Shutdown the worker pool"""
        self.executor.shutdown(wait=wait)


def parallel_map(
    items: List[Any],
    func: Callable,
    max_workers: int = 4,
    timeout: float = 30.0
) -> List[Any]:
    """
    Parallel map function over items
    
    Example:
        results = parallel_map(
            items=resumes,
            func=extract_resume_text,
            max_workers=8
        )
    """
    results = [None] * len(items)
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(func, item): idx
            for idx, item in enumerate(items)
        }
        
        for future in as_completed(futures, timeout=timeout):
            idx = futures[future]
            try:
                results[idx] = future.result()
            except Exception as e:
                results[idx] = None
                logging.error(f"Error processing item {idx}: {e}")
    
    return results


# Convenience decorators
def run_async(func: Callable):
    """Decorator to run function in background thread"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        thread = threading.Thread(
            target=func,
            args=args,
            kwargs=kwargs,
            daemon=True
        )
        thread.start()
        return thread
    return wrapper


def run_in_thread_pool(max_workers: int = 4):
    """Decorator to submit function to thread pool"""
    pool = ThreadPoolExecutor(max_workers=max_workers)
    
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return pool.submit(func, *args, **kwargs)
        return wrapper
    return decorator
