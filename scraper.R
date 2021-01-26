request(httr)
request(rvest)
request(xml2)
request(stringr)
request(stringi)
request(openxlsx)

#### Scraper de dados do VACINOMETRO da Prefeitura Municipal de Feira de Santana

url <- "http://www.feiradesantana.ba.gov.br/coronavirus/vacinometro/"

html <- read_html(url)
header <- html %>% 
  html_nodes("h4") %>%
  html_text()

data <- unlist(strsplit(header[3]," "))[3]

numbers <- html %>% 
  html_nodes("h2") %>%
  html_text()

vacinas_total <- unlist(strsplit(numbers[1],"\r"))[1] %>% 
  stringr::str_replace_all("[.]","") %>% 
  as.numeric()
n_marcas_vacinas <- length(unlist(strsplit(numbers[1], "\r"))) -2
df_vacinas_por_marca <- data.frame()
for(i in 1:n_marcas_vacinas){
  marca <- unlist(strsplit(numbers[1],"\r"))[i+2] %>% stringi::stri_extract_last_words()
  n_vacinas <- unlist(strsplit(numbers[1],"\r"))[i+2] %>% 
    stringi::stri_extract_first_words() %>%
    stringr::str_replace_all("[.]","") %>% 
    as.numeric()
  df_vacinas_por_marca <- rbind(df_vacinas_por_marca, data.frame(marca, n_vacinas))
}

vacinados_total <- numbers[2] %>% 
  stringr::str_replace_all("[.]","") %>% 
  as.numeric()
vacinados_hoje <- numbers[3] %>% 
  stringr::str_replace_all("[.]","") %>% 
  as.numeric()


#### OUTPUT

df_output <- data.frame(data = data,
                        total_vacinas = vacinas_total)

n_vacinas_marcas <- cbind(df_vacinas_por_marca[,2])
nomes_vacinas_marcas <- paste0("vacina-",cbind(df_vacinas_por_marca[,1]))
aux_df <- data.frame(rbind(n_vacinas_marcas[,1]))
names(aux_df) <- nomes_vacinas_marcas

df_output <- cbind(df_output,
                   aux_df)

df_output$total_vacinados <- vacinados_total
df_output$vacinados_hoje <- vacinados_hoje

write.table(df_output, "dados_vacinometro_fsa.csv", sep = ",", col.names = !file.exists("dados_vacinometro_fsa.csv"), append = T, row.names=FALSE)

