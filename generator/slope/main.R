source("./config.R")
source("./utils.R")


get_country_prefix = function(country_name){
  switch(country_name,
         "tanzania"="TZ0"
         )
}


project_files = function(country_name){
  # this function makes sure that all the files have the same 
  # resolution = 10km and projection. 
 

    point_file = shapefile(point_files[5])
    country_slope_dir = paste0(slope_dir,country_name)
    slope_files =  get_files(country_slope_dir)
  
    
    slope = projectRaster(raster(slope_files[1]), crs=crs(point_file), method="ngb")
    slope_length = projectRaster(raster(slope_files[9]), crs=crs(point_file), method="ngb")
  
    point_files = get_files(points_dir)
    country_sol_prefix = get_country_prefix(country_name)
  
    
    
    country_map = substr(point_file$SoilProfil,1,3) == country_sol_prefix
    country_point_file = point_file[country_map,]

    dummy_ras = raster(ncols=dim(slope)[2], nrows=dim(slope)[1], res=c(10000,10000))
    country_point_file_prj = spTransform(country_point_file,crs(slope))
    #country_point_file_prj$SoilProfil = sanitize_ids(country_point_file_prj$SoilProfil)
    point_raster= rasterize(country_point_file_prj,slope_length,field="CELL5M")
    
    slopes_st = stack(slope,slope_length)
    res_st = stack(point_raster,slopes_st)
    
    
    
    res_df = as.data.frame(res_st)
    names(res_df) = c("id","slope","slope_length")
    mask = !is.na(res_df$id)
    res_df_id = res_df[mask,]
    slope_info_path = paste0(slope_dir,"slope_info.csv")
    write.csv(res_df_id,slope_info_path,row.names = F)
    log("Finished") 
   
}


args = commandArgs(trailingOnly = TRUE)
country_name = args[1]
project_files(country_name)





