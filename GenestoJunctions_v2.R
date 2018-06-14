#GenestoJunctions_v2.R: The next code will get the unique genes associated to each junction and will associate this list of genes to each junctions in the original bed file
#Additionally, we will study the type of each junction (1: Annotated, 2: New connection, 3: 5ss, 4: 3ss, 5: New junction)
#V2: This version has been adapted for been used for change_gtf.sh

#arg[1]: Scripts dir --> Root to the path of Junckey scripts
#arg[2]: Input file --> SJ.out.bed: file with all the junctions
#arg[3]: Input file --> SJ.out.enriched.unique.bed: file with the junctions which falls in exons, according to the annotation
#arg[4]: Input file --> SJ.out.enriched.filtered.bed: file with the exons that overlaps exactly with the junction
#arg[5]: Ouput file --> SJ.out.junction.type.bed: output file with the list junction and the type of each junction
#arg[6]: Output file --> SJ.out.geneAnnotated.bed: output file with the whole information

#install.packages("data.table")
suppressMessages(require(data.table))

########################
#Gene annotation
########################

cat("\tGenestoJunctions_v2.R: Gene annotation...\n")
CHARACTER_command_args <- commandArgs(trailingOnly=TRUE)

scripts_path <- CHARACTER_command_args[1]
# scripts_path <- "/genomics/users/juanluis/comprna/Junckey"

original_file_bed <- fread(CHARACTER_command_args[2])
# original_file_bed <- fread("/projects_rg/SCLC_cohorts/George/STAR/v2/S00035T/SJ.out.bed")
colnames(original_file_bed) <- c("chrom","start","end","id","unique_junction_reads","strand","annotated")
original_file_bed <- as.data.frame(original_file_bed)

file_unique <- fread(CHARACTER_command_args[3],header=FALSE,sep=" ")
# file_unique <- fread("/projects_rg/SCLC_cohorts/George/STAR/v2/S00035T/SJ.out.enriched.unique.bed",header=FALSE,sep=" ")
file_unique <- as.data.frame(file_unique)

#Remove the " and ; from the genes column
file_unique$V2 <- unlist(lapply(file_unique$V2,function(x)gsub("\"|\\;","",x,perl=TRUE)))

#Remove those with 0 gene associated
file_unique_f <- file_unique[which(file_unique$V2!="0"),]

#There are ids with more than one gene associated
table <- table(as.character(file_unique_f$V1))
duplicated_ids <- row.names(table[which(table!=1)])
duplicated_ids2 <- file_unique_f[which(as.character(file_unique_f$V1)%in%duplicated_ids),]
table2 <- table(as.character(duplicated_ids2$V1))

#For each id, take all the id genes and paste it in one line
id <- ""
list_genes <- ""
matrix_output <- matrix(data="",nrow=length(table2),ncol=2)
colnames(matrix_output) <- c("Id","Genes")
cont <- 1
i <- 1
for(i in 1:nrow(duplicated_ids2)){
  if(i==1){
    id <- as.character(duplicated_ids2[i,]$V1)
    list_genes <- as.character(duplicated_ids2[i,]$V2)
  }
  else if(id!=as.character(duplicated_ids2[i,]$V1)){
    matrix_output[cont,1] <- id
    matrix_output[cont,2] <- list_genes
    cont <- cont + 1
    id <- as.character(duplicated_ids2[i,]$V1)
    list_genes <- as.character(duplicated_ids2[i,]$V2)
  }
  else{
    list_genes <- paste0(list_genes,",",as.character(duplicated_ids2[i,]$V2))
  }
}
matrix_output[cont,1] <- id
matrix_output[cont,2] <- list_genes

df_output <- as.data.frame(matrix_output)

#Associate this lists to the original SJ.out.enriched.unique.bed
file_unique2 <- merge(file_unique_f,df_output,by.x="V1",by.y="Id",all.x=TRUE)
file_unique2$Genes_final <- ifelse(is.na(file_unique2$Genes),as.character(file_unique2$V2),as.character(file_unique2$Genes))
file_unique3 <- unique(file_unique2[,c("V1","Genes_final")])

#Associate this info to the original bed file
original_file_bed_final <- merge(original_file_bed,file_unique3,by.x="id",by.y="V1",all.x=TRUE)
colnames(original_file_bed_final)[8] <- "Associated_genes"
# write.table(original_file_bed_final,file=CHARACTER_command_args[3],sep="\t",quote=FALSE,row.names=FALSE)

########################
#Type of the junctions
########################

#Call the next python script for obtaining the type of our junctions
work.dir <- getwd()
system(paste0("python ", scripts_path, "/GenestoJunctions.py ",CHARACTER_command_args[4], " ",CHARACTER_command_args[5]))
output_df <- as.data.frame(fread(CHARACTER_command_args[5],header = FALSE))
#Associate this info to the original bed file
original_file_bed_final2 <- merge(original_file_bed_final,output_df,by.x="id",by.y="V1",all.x=TRUE)
colnames(original_file_bed_final2)[9] <- "Type_junction"
original_file_bed_final2$Type_junction <- ifelse(is.na(original_file_bed_final2$Type_junction),5,original_file_bed_final2$Type_junction)
write.table(original_file_bed_final2,file=CHARACTER_command_args[6],sep="\t",quote=FALSE,row.names=FALSE)
cat("\tGenestoJunctions_v2.R: Saved SJ.out.geneAnnotated.bed\n")
cat("\tGenestoJunctions_v2.R: Finish\n")
