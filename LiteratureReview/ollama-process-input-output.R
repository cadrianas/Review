library(ollamar)
library(bibtex)

process_bib_file_ollama = function(infile, INPUT, OUTPUT) {
  # Need to check if local arborescence exists. So first decompose 
  # file name with local arborescence info
  tmp = strsplit(infile, "/")[[1]]
  # First entry is /, discard. Also discard last entry (file name)
  dirs = tmp[2:(length(tmp)-1)]
  # Go down in arborescence and check existence of directories while doing so
  for (level in 1:length(dirs)) {
    if (level == 1) {
      curr_dir = paste0(OUTPUT, "/", dirs[level])
    } else {
      curr_dir = paste0(curr_dir, "/", dirs[level])
    }
    if (!dir.exists(curr_dir)) {
      dir.create(curr_dir)
    }
  }
  # Now read in the bib file
  bib_entry = read.bib(paste0(INPUT, infile))
  # Is there an abstract? If not, don't do anything.
  abstract = bib_entry[1]$abstract
  if (!is.null(abstract)) {
    model = "llama2:13b"
    authors = bib_entry[1]$author
    base_message = "Summarize the following abstract in 200 words or less; do not say anything but the summary. "
    message = paste0(base_message, 
                     "Abstract: ", abstract)
    output = generate(model = model,
                      prompt = message,
                      stream = FALSE,
                      output = "df")
    output = output$response
  } else {
    output = "No abstract in the bib file"
  }
  # Write output to file
  writeLines(output, paste0(OUTPUT, infile))
}

INPUT = "/home/cadrianas/NAS-small-DATA/adriana-llm-reviews/bib-files"
OUTPUT = "/home/cadrianas/NAS-small-OUTPUT/adriana-llm-reviews/bib-files"

list_files_input = data.frame(
  fqfn = list.files(INPUT, 
                    pattern = ".bib", 
                    full.names = TRUE,
                    recursive = TRUE)
)
# We need the directory structure relative to the top directory 
# in INPUT and OUTPUT to compare files in both arborescences
list_files_input$subdir_fn = gsub(INPUT, "", 
                                  list_files_input$fqfn)

# We loop until all files are processed (we use break to exit the loop)
while (TRUE) {
  list_files_output = data.frame(
    fqfn = list.files(OUTPUT, 
                      pattern = ".bib", 
                      full.names = TRUE,
                      recursive = TRUE)
  )
  list_files_output$subdir_fn = gsub(OUTPUT, "", 
                                     list_files_output$fqfn)
  # We need to process the files that are in INPUT but not in OUTPUT
  # Do differences based on the relative path in the arborescence
  to_process = setdiff(list_files_input$subdir_fn, 
                       list_files_output$subdir_fn)
  # Now find index of these files in list_files_input
  index_to_process = match(to_process, list_files_input$subdir_fn)
  to_process_df = list_files_input[index_to_process,]
  # If there are no files to process, we stop
  if (nrow(to_process_df) == 0) {
    break
  } else {
    # We process a file. Pick a random one..
    idx = sample.int(nrow(to_process_df), 1)
    # Talk a little
    writeLines(paste0("Currently ", 
                      nrow(to_process_df), 
                      " files left to process, processing file number ",
                      idx))
    # Use for debugging (to use in the function)
    # infile = to_process_df$subdir_fn[idx]
    # Process
    process_bib_file_ollama(to_process_df$subdir_fn[idx], 
                            INPUT, OUTPUT)
  }
}
