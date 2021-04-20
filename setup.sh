mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"${julihocsman@gmail.com}\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS = false\n\
enableWebsocketCompression=false\n\
enableXsrfProtection=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
