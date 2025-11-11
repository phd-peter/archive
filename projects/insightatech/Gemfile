source 'https://rubygems.org'

gem 'jekyll', '~> 4.3.0'
gem 'jekyll-paginate', '1.1.0'
gem 'jekyll-spaceship', '0.10.2'
gem 'webrick', '1.8.2'

# Ruby 3.4 compatibility gems
gem 'logger'
gem 'csv'
gem 'base64'
gem 'bigdecimal'

# Windows and JRuby does not include zoneinfo files, so bundle the tzinfo-data gem
# and associated library.
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end

# Performance-booster for watching directories on Windows (skip if causing issues)
# gem "wdm", "~> 0.1.1", :platforms => [:mingw, :x64_mingw, :mswin]