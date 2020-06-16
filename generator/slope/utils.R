log <- function(...){
  arguments <- paste(list(...),collapse= ' ')
  print(arguments)
  
}

get_files = function(path,ptn="*", full_path=T){
  # returns the paths of all the files inside a particular directory path
  
  # Parameters - 
  
  # path = directory path
  # ptn = pattern to find 
  
  files = list.files(path,pattern=glob2rx(ptn), full.names = full_path)
  return(files)
}