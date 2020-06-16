import_libs = function(){
  library(rgdal)
  library(raster)
  library(reshape2)
  library(parallel)
  library(snow)
  library(gdata)
  library(data.table)
}

root_dir = "/gpfs/data1/cmongp/ujjwal/tanzania/tanzania_soil/generator/slope/"
points_dir = paste0(root_dir,"point_files/")
slope_dir = paste0(root_dir, "slope_files/")


import_libs()


