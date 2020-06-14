from abc import ABC, abstractmethod

class TCDExport(ABC):
   """
   TODO:
   -Upon success/failed connection give a useful message/feedback
   -Validate input to see if it looks like the pattern we expect if not tell the user what we expect
   Documentation:
   This is method needs to be invoked before any of the other methods can be used in the class
   comport param is a string passed from the user, which indicated where the TCD port is being streamed from e.g. COMPORT1.
   """
   @abstractmethod
   def com_port_connection(self):
       pass

   """
   TODO:
   -When starting stream give success/fail message of start,
   -Things to consider filepath may not exists
   Doc:
   Starts streaming to csv file, the file will be open during this time, and will be locked.
   """
   @abstractmethod
   def start_csv_data_export(self):
       pass

   """
   TODO:
   -When starting stream give success/fail message of start,
   -Things to consider HTTP connection could fail
   -Support secure connection
   Doc:
   Starts streaming to HTTP endpoint given, will keep the socket connection open
   """
   @abstractmethod
   def start_http_data_export(self):
       pass

   """
   Doc:
   Closes the opened file stream and unlocks, this needs to be done before reading/opening file
   """
   @abstractmethod
   def stop_csv_data_export(self):
       pass

   """
   Doc:
   Closes the socket connection of the HTTP endpoint
   """
   @abstractmethod
   def stop_http_data_export(self):
       pass
