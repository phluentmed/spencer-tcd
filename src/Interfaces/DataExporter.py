from abc import ABC, abstractmethod

class DataExporter(ABC):

   """
   Starts streaming data to a destination. Returns 0 on success and a negative
   error code on failure.
   """
   @abstractmethod
   def start(self):
       pass
   """
   Stops data export, and safely closes off destination.
   """
   @abstractmethod
   def stop(self):
       pass
   """
   Receives data to be exported
   @param
   data: decoded data format 
   @param
   result_handler: called after the data export operation is completed.
   """
   @abstractmethod
   def export(self, data, result_handler):
       pass
