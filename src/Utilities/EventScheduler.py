from enum import Enum
import sched
import sys
# import time
import threading

# Refer to sched.scheduler for a description of non-modified functions
class EventScheduler(sched.scheduler):

    class QueueStatus(Enum):
        STARTED = 0
        STOPPING = 1
        STOPPED = 2

    def __init__(self):
        super().__init__(self)
        self._queue_status_lock = threading.RLock()
        self._queue_status = QueueStatus.STOPPED
        self._csv_thread = threading.Thread(target=self.run, name="csv_thread")

    def enterabs(self, time, priority, action, argument=(), kwargs=_sentinel):
        """Enter a new event in the queue at an absolute time.
        Returns an ID for the event which can be used to remove it,
        if necessary.
        """
        with self._queue_status_lock:
            if self._queue_status != QueueStatus.STARTED:
                # TODO: Raise an error here or have a status code with failure
                # message.
                return
            return super().enterabs(time, priority, action, argument, kwargs)

    def enter(self, delay, priority, action, argument=(), kwargs=_sentinel):
        """A variant that specifies the time as a relative time.
        This is actually the more commonly used interface.
        """
        with self._queue_status_lock:
            if self._queue_status != QueueStatus.STARTED:
                # TODO: Raise an error here or have a status code with failure
                # message.
                return
            return super().enter(delay, priority, action, argument, kwargs)

    def cancel(self, event):
        """Remove an event from the queue.
        This must be presented the ID as returned by enter().
        If the event is not in the queue, this raises ValueError.
        """
        with self._queue_status_lock:
            if self._queue_status != QueueStatus.STARTED:

                # TODO: Raise an error here or have a status code with failure
                # message.
                return -1, "EventScheduler is not running."
        super().cancel(event)
        return 0

    def empty(self):
        pass

    def run(self):
        # Taken from the python library and slightly modified for an
        # always-on event scheduler. SHOULD NOT BE CALLED DIRECTLY.

        """Execute events until the queue is empty.
        If blocking is False executes the scheduled events due to
        expire soonest (if any) and then return the deadline of the
        next scheduled call in the scheduler.
        When there is a positive delay until the first event, the
        delay function is called and the event is left in the queue;
        otherwise, the event is removed from the queue and executed
        (its action function is called, passing it the argument).  If
        the delay function returns prematurely, it is simply
        restarted.
        It is legal for both the delay function and the action
        function to modify the queue or to raise an exception;
        exceptions are not caught but the scheduler's state remains
        well-defined so run() may be called again.
        A questionable hack is added to allow other threads to run:
        just after an event is executed, a delay of 0 is executed, to
        avoid monopolizing the CPU when other threads are also
        runnable.
        """
        # localize variable access to minimize overhead
        # and to improve thread safety
        lock = self._lock
        q = self._queue
        delayfunc = self.delayfunc
        timefunc = self.timefunc
        pop = heapq.heappop
        while True:
            with lock:
                if not q:
                    continue
                time, priority, action, argument, kwargs = q[0]
                if priority == sys.maxsize:
                    pop(q)
                    break
                now = timefunc()
                if time > now:
                    delay = True
                else:
                    delay = False
                    pop(q)
            if delay:
                delayfunc(time - now)
            else:
                action(*argument, **kwargs)
                delayfunc(0)   # Let other threads run

    def start(self):
        with self._queue_status_lock:
            if self._queue_status != QueueStatus.STOPPED:
                # TODO: Raise an error here or have a status code with failure
                # message.
                return -1, "EventScheduler has already started or is stopping."
            self._csv_thread.start()
            self._queue_status = QueueStatus.STARTED
        return 0

    def stop(self):
        with self._queue_status_lock:
            if self._queue_status != QueueStatus.STARTED:
                # TODO: Raise an error here or have a status code with failure
                # message
                return -1, "EventScheduler is stopped or stopping."
            self._queue_status = QueueStatus.STOPPING
        self.enterabs(self.timefunc( )+ self.timefunc(), # TODO: Fix this
                      sys.maxsize,                       # hackiness
                      None)
        with self._queue_status_lock:
            self._csv_thread.join()
            self._queue_status = QueueStatus.STOPPED
        return 0

    @property
    def queue(self):
        """An ordered list of upcoming events.
        Events are named tuples with fields for:
            time, priority, action, arguments, kwargs
        """
        # Use heapq to sort the queue rather than using 'sorted(self._queue)'.
        # With heapq, two events scheduled at the same time will show in
        # the actual order they would be retrieved.
        pass