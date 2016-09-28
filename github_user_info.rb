# require File.join File.dirname(__FILE__), 'http_to_json'
require './http_to_json'
require 'httpclient'
require 'json'

print "Please input your GitHub username: "
user = gets.chomp
user_url = "https://api.github.com/users/#{user}"
repos_url = "https://api.github.com/users/#{user}/repos"

puts "This may take a while 0/? repositories"

# converting the json from github api to hashes
user_json = http_to_json(user_url)
repos_json = http_to_json(repos_url)

print "This may take a while 0/#{repos_json.length} repositories \r"
$stdout.flush
languages = Hash.new

# looping over all the repos
i = 0
while i < repos_json.length
  repo_name = repos_json[i]["name"]
  languages_url = "https://api.github.com/repos/#{user}/#{repo_name}/languages"
  languages_json = http_to_json(languages_url)
  print "This may take a while. #{i+1}/#{repos_json.length} repositories \r"
  $stdout.flush
  # looping over all the languages in each repo
  j = 0
  while j < languages_json.length
    # if it doesn't exist, adds a language and its value to languages hash
    if languages["#{languages_json.keys[j]}"] == nil
      languages["#{languages_json.keys[j]}"] = languages_json.values[j]
    #else append the values of a language to existing value
    else
      languages["#{languages_json.keys[j]}"] += languages_json.values[j]
    end
    j += 1
  end
  i += 1
end
puts
puts
# looping over the languages hash and displaying all the languages in a readable manner.
i = 0
while i < languages.length
  puts "#{languages.keys[i]}: \n \t#{languages.values[i]} bytes ~= #{languages.values[i]/1000} kB. \n \t#{languages.values[i]/25} lines roughly."
  puts
  i += 1
end
