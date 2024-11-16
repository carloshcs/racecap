mkdir -p ~/.streamlit/ 
"echo \"[server]\nheadless = true\nport = \$PORT\nenableCORS=false\" > ~/.streamlit/config.toml" 

echo "\
[general]\n\
email = \"carloshcsaunders@gmail.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml