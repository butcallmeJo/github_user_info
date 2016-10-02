require 'httpclient'
require 'json'

def http_to_json(url)

  extheaders = {
    'User-Agent' => 'Holberton_School',
    'Authorization' => 'token fffa38b10948aa7eff293682308672bc95672ae3'
  }

  http = HTTPClient.new
  response = http.get(url, nil, extheaders)

  # error handling and exiting if wrong status
  if response.status != 200
    puts "Invalid username or bad server response."
    puts "server code: #{response.status}"
    abort
  end

  return json = JSON.parse(response.content)

end
