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
  
    country_slope_dir = paste0(slope_dir,country_name)
    slope_files =  get_files(country_slope_dir)
  
    slope = raster(slope_files[1])
    slope_length = raster(slope_files[7])
  
    point_files = get_files(points_dir)
    country_sol_prefix = get_country_prefix(country_name)
  
    
    point_file = shapefile(point_files[5])
    country_map = substr(point_file$SoilProfil,1,3) == country_sol_prefix
    country_point_file = point_file[country_map,]

    dummy_ras = raster(ncols=dim(slope)[2], nrows=dim(slope)[1], res=c(10000,10000))
    country_point_file_prj = spTransform(country_point_file,crs(slope))
    #country_point_file_prj$SoilProfil = sanitize_ids(country_point_file_prj$SoilProfil)
    point_raster= rasterize(country_point_file_prj,slope,field="CELL5M")
    
    slopes_st = stack(slope,slope_length)
    res_st = stack(point_raster,slopes_st)
    
    ras_na <- function(r,xy){
      apply(X=xy, MARGIN=1,
            FUN = function(xy) r@data@values[which.min(replace(distanceFromPoints(r, xy),
                                                               is.na(r),NA))])
    }
    
    lapply(res_st@layers, function(a_layer) ras_na(a_layer,xy))
    
    
    res_df = as.data.frame(res_st)
    names(res_df) = c("id","slope","slope_length")
    mask = !is.na(res_df$id)
    res_df_id = res_df[mask,]
    slope_info_path = paste0(slope_dir,"slope_info.csv")
    write.csv(res_df_id,slope_info_path,row.names = F)
    
}

main = function(){
  project_files(country_name)
  convert_points_file
}
