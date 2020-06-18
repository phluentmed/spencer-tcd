from abc import ABC, abstractmethod

class DataExporter(ABC):

   """
   Starts streaming data to a destination.
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
   result_handler:
   """
   @abstractmethod
   def export(self, data, result_handler):
       pass
