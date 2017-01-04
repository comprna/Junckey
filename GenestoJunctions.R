#!/soft/R/R-3.2.3/bin/Rscript

#GenestoJunctions.R: The next code will get the unique genes associated to each junction and will associate this list of genes to each junctions in the original bed file
#Additionally, we will study the type of each junction (1: Annotated, 2: New connection, 3: 5ss, 4: 3ss, 5: New junction)
#arg[1]: Input file --> SJ.out.bed: file with all the junctions
#arg[2]: Input file --> SJ.out.enriched.unique.bed: file with the junctions which falls in exons, according to the annotation
#arg[3]: Input file --> SJ.out.enriched.filtered.bed: file with the exons that overlaps exactly with the junction
#arg[4]: Output file --> SJ.out.geneAnnotated.bed: input file with the list of genes per junction and the type of each junction

library(data.table)

########################
#Gene annotation
########################

CHARACTER_command_args <- commandArgs(trailingOnly=TRUE)

original_file_bed <- fread(file=CHARACTER_command_args[1])
colnames(original_file_bed) <- c("chrom","start","end","id","unique_junction_reads","strand","annotated")

file_unique <- fread(file=CHARACTER_command_args[2],fill=TRUE)

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
i <- 3
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

# Load the file with the junctions that overlapps exactly with the exons
original_file_bed_filtered <- fread(file=CHARACTER_command_args[3],sep="\t")

#Do the unique from just the exons
original_file_bed_filtered2 <- unique(original_file_bed_filtered[,c(-5,-9,-10,-13:-22)])

#Count the number of rows per juntions
number_rows <- table(original_file_bed_filtered2$V4)

output_matrix <- matrix(data="",nrow=length(number_rows),ncol=2)
cont_matrix <- 1
i <- 1
flag_Anno <- 0
flag_5s <- 0
flag_3s <- 0
id <- ""
while(i<=nrow(original_file_bed_filtered2)){
  if(i==1){
    id <- as.character(original_file_bed_filtered2[i,]$V4)
  }
  #Check if we have change the id
  else if(id!=as.character(original_file_bed_filtered2[i,]$V4)){
    #According to the flags, output to the output_matrix
    if(flag_Anno==1){
      #Case 1: Annotated junction
      output_matrix[cont_matrix,1] <- id
      output_matrix[cont_matrix,2] <- 1
      cont_matrix <- cont_matrix + 1
      id <- as.character(original_file_bed_filtered2[i,]$V4)
      flag_Anno <- 0
      flag_5s <- 0
      flag_3s <- 0
    }
    else if(flag_5s==1 & flag_3s==1){
      #Case 2: New connection (from annotated exons)
      output_matrix[cont_matrix,1] <- id
      output_matrix[cont_matrix,2] <- 2
      cont_matrix <- cont_matrix + 1
      id <- as.character(original_file_bed_filtered2[i,]$V4)
      flag_Anno <- 0
      flag_5s <- 0
      flag_3s <- 0
    }
    else if(flag_5s==1 & flag_3s==0){
      #Case 3: A5ss
      output_matrix[cont_matrix,1] <- id
      output_matrix[cont_matrix,2] <- 3
      cont_matrix <- cont_matrix + 1
      id <- as.character(original_file_bed_filtered2[i,]$V4)
      flag_Anno <- 0
      flag_5s <- 0
      flag_3s <- 0
    }
    else if(flag_5s==0 & flag_3s==1){
      #Case 4: A3ss
      output_matrix[cont_matrix,1] <- id
      output_matrix[cont_matrix,2] <- 4
      cont_matrix <- cont_matrix + 1
      id <- as.character(original_file_bed_filtered2[i,]$V4)
      flag_Anno <- 0
      flag_5s <- 0
      flag_3s <- 0
    }
    else{
      print("ERROR: Case not studied")
      output_matrix[cont_matrix,1] <- id
      output_matrix[cont_matrix,2] <- 0
      cont_matrix <- cont_matrix + 1
      id <- as.character(original_file_bed_filtered2[i,]$V4)
      flag_Anno <- 0
      flag_5s <- 0
      flag_3s <- 0
    }
  }
  
  #Now, check the new line  
  #Case 1: If annotated = 1 --> Annotated conection
  if(original_file_bed_filtered2[i,]$V7==1){
    flag_Anno <- 1
  }
  #If annotated = 0
  else{
    #We have to test if the junctions is mapping the 5', the 3' or both
    if(original_file_bed_filtered2[i,]$V2==original_file_bed_filtered2[i,]$V12-1){
      flag_5s <- 1
    }
    else if(original_file_bed_filtered2[i,]$V3==original_file_bed_filtered2[i,]$V11){
      flag_3s <- 1
    }
  }
  i <- i + 1
}


#According to the flags, output to the output_matrix
if(flag_Anno==1){
  #Case 1: Annotated junction
  output_matrix[cont_matrix,1] <- id
  output_matrix[cont_matrix,2] <- 1
}
if(flag_5s==1 & flag_3s==1){
  #Case 2: New connection (from annotated exons)
  output_matrix[cont_matrix,1] <- id
  output_matrix[cont_matrix,2] <- 2
}
if(flag_5s==1 & flag_3s==0){
  #Case 3: A5ss
  output_matrix[cont_matrix,1] <- id
  output_matrix[cont_matrix,2] <- 3
}
if(flag_5s==0 & flag_3s==1){
  #Case 4: A3ss
  output_matrix[cont_matrix,1] <- id
  output_matrix[cont_matrix,2] <- 4
}

output_df <- as.data.frame(output_matrix)


#Associate this info to the original bed file
original_file_bed_final2 <- merge(original_file_bed_final,output_df,by.x="id",by.y="V1",all.x=TRUE)
colnames(original_file_bed_final2)[9] <- "Type_junction"
original_file_bed_final2$Type_junction <- ifelse(is.na(original_file_bed_final2$Type_junction),5,original_file_bed_final2$Type_junction)
write.table(original_file_bed_final2,file=CHARACTER_command_args[4],sep="\t",quote=FALSE,row.names=FALSE)
