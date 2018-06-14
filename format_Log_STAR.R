#Get the total mapped reads per sample and the average_length. Given the input of 
# all the Log.final.out files from STAR output, this script will generate the next output:
#   -   totalMappedReads.tab 
#   -   averageLength.tab

CHARACTER_command_args <- commandArgs(trailingOnly=TRUE)

# CHARACTER_command_args <- "/projects_rg/Bellmunt/STAR/TEST/*"
log_files <- system(paste0("ls ",CHARACTER_command_args[1],"*/Log.final.out"),intern=TRUE)
log_files2 <- lapply(log_files,function(x)strsplit(x, split="/"))
log_files3 <- lapply(log_files2,function(x)x[[1]][length(log_files2[[1]][[1]])-1])
total_mapped_reads <- matrix(data="",nrow=length(log_files),ncol=2)
average_length <- matrix(data="",nrow=length(log_files),ncol=2)

i <- 1
for(i in 1:length(log_files)){
  log_file <- read.table(file=log_files[i],fill=TRUE,sep="\t")
  total_mapped_reads[i,1] <- unlist(log_files3[i])
  total_mapped_reads[i,2] <- as.character(log_file[8,2])
  average_length[i,1] <- unlist(log_files3[i])
  average_length[i,2] <- as.character(log_file[10,2])
}

#Generate the output
write.table(total_mapped_reads,file=paste0(CHARACTER_command_args[2],"totalMappedReads.tab"),sep="\t",quote=FALSE,row.names = FALSE, col.names = FALSE)
write.table(average_length,file=paste0(CHARACTER_command_args[2],"averageLength.tab"),sep="\t",quote=FALSE,row.names = FALSE, col.names = FALSE)
