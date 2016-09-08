require 'date'
require 'pathname'
require 'shellwords'
require 'shell'

PUBLISHED_DIR = Pathname 'catalog'
WRANGLE_DIR = Pathname 'wrangle'
SCRIPTS_DIR = WRANGLE_DIR.join('scripts')
FETCHED_DIR = WRANGLE_DIR.join('corral', 'fetched')

START_DATE = DateTime.new(1960, 1)
END_DATE = DateTime.now()
ALL_YEAR_MONTHS = START_DATE.upto(END_DATE).map{|d| d.strftime('%Y-%m')}.uniq()
USCOORDS = {lng0: -125, lng1: -65, lat0: 24.6, lat1: 50}
OKCOORDS = {lng0: -106.743, lng1: -90.659, lat0: 31.075, lat1: 41}

PACKAGES = {
  :decades => (1960..2000).step(10),
  :periods => [(2010..2014),],        # too big for a decade
  :years => 2015...END_DATE.year      # each of these years are too big for a single file
}

# will convert this rakefile into standard conventions later
P_FILES  = {
  'ytd' => PUBLISHED_DIR / "usgs-earthquakes-#{END_DATE.year}.csv"
}


def enum_yearmonths(dx, dy)
  """Returns a list of strings between dx and dy (which are DateTimes),
     e.g. for 2010-01 and 2010-03,  2010-01, 2010-02 2010-03
  """
  return dx.upto(dy).map{|d| d.strftime('%Y-%m')}.uniq()
end



task :default => [:refresh]

desc 'setup the directories'
task :setup do
  puts "Creating directories"
  [PUBLISHED_DIR, SCRIPTS_DIR, FETCHED_DIR].each{|p| p.mkpath}
end


desc "re-fetch the two most recent months and repackage the most recent year"
task :refresh do
  Rake::Task[P_FILES['ytd']].invoke
  enum_yearmonths(END_DATE - 31, END_DATE).each do |ym|
    Rake::Task['fetch:yearmonth'].execute(:yearmonth => ym)
  end
end


# Packaged files
# decade files

namespace :publish do
  # e.g. decade-1970.csv
  PACKAGES[:decades].each do |decade|
    # e.g. 1970-01 to 1979-12
    yms = enum_yearmonths(DateTime.new(decade, 1), DateTime.new(decade+9, 12))
    srcnames = yms.map{|x| FETCHED_DIR.join "#{x}.csv"}
    destname = PUBLISHED_DIR.join("usgs-earthquakes-decade-#{decade}.csv").to_s
    desc "Package decade of #{decade}"
    file destname => srcnames do
      cmd1 = Shellwords.join(['python', SCRIPTS_DIR.join('compile_years.py'),
                               decade, decade + 10, FETCHED_DIR])
      Shell.new.system(cmd1) > String(destname)

    end
  end

  # e.g. 2010-2014.csv
  PACKAGES[:periods].each do |period|
    px = period.first
    py = period.last
    pyms = (px..py).map{ |y| (1..12).map{|m| "#{y}-#{"%02d" % m}"}}.flatten()
    srcnames = pyms.map{ |ym| FETCHED_DIR.join "#{ym}.csv"}
    collated_through_filename = PUBLISHED_DIR.join "usgs-earthquakes-#{px}-through-#{py}.csv"
    desc "Package earthquakes from #{px} through #{py}"
    file collated_through_filename => srcnames do
      cmd1 = Shellwords.join(['python', SCRIPTS_DIR.join('compile_years.py'),
                               px, py + 1, FETCHED_DIR])
      Shell.new.system(cmd1) > String(collated_through_filename)

    end
  end

  # e.g. 2016.csv
  PACKAGES[:years].each do |year|
    yms = enum_yearmonths(DateTime.new(year, 1), DateTime.new(year, 12))
    srcnames = yms.map{|s| FETCHED_DIR.join(s + '.csv')}
    destname = PUBLISHED_DIR.join "usgs-earthquakes-#{year}.csv"
    desc "package single year #{year}"
    file destname => srcnames do
      cmd1 = Shellwords.join(['python', SCRIPTS_DIR.join('compile_years.py'),
                               year, year + 1, FETCHED_DIR])
      Shell.new.system(cmd1) > String(destname)

    end
  end



  ### Special case for the current year
  desc "Year to date: #{END_DATE.year}"
  yms = enum_yearmonths(DateTime.new(END_DATE.year, 1), END_DATE)
  srcnames = yms.map{|s| FETCHED_DIR.join(s + '.csv')}
  file P_FILES['ytd'] => srcnames do
    cmd1 = Shellwords.join(['python', SCRIPTS_DIR.join('compile_years.py'),
                                      END_DATE.year, END_DATE.year+1, FETCHED_DIR])
    # the most recent year isn't complete, so we don't depend
    # on the entire year's worth of month files being fetched
    Shell.new.system(cmd1) > String(P_FILES['ytd'])
  end


  # time periods, contiguous united states
  # e.g. contiguous-united-states-2000-through-2015.csv
  [[1970, 1999],[2000, 2015]].each do |period|
    px = period.first
    py = period.last
    pyms = (px..py).map{ |y| (1..12).map{|m| "#{y}-#{"%02d" % m}"}}.flatten()
    srcnames = pyms.map{ |ym| FETCHED_DIR.join "#{ym}.csv"}
    us_contiguous_fname = PUBLISHED_DIR.join "usgs-earthquakes-contiguous-united-states-#{px}-through-#{py}.csv"
    desc "Filter for earthquakes within contiguous United States"
    file us_contiguous_fname => srcnames do
      cmd1 = Shellwords.join(['python', SCRIPTS_DIR.join('compile_years.py'),
                                    px, py + 1, FETCHED_DIR])
      cmd2 = Shellwords.join(['python', SCRIPTS_DIR.join('filter_bounding_box.py'),
                                   USCOORDS[:lng0], USCOORDS[:lat0], USCOORDS[:lng1],
                                   USCOORDS[:lat1], '-'])
      shell = Shell.new
      shell.system(cmd1) | shell.system(cmd2) > us_contiguous_filename.to_s
    end
  end


  # Oklahoma region earthquakes
  desc "Collect all earthquakes around Oklahoma"
  # assuming :fetched dir is full...
  ok_filename = PUBLISHED_DIR.join "usgs-earthquakes-oklahoma-region.csv"

  file ok_filename do
    cmd = ["cat", FETCHED_DIR / '*.csv', '|',
            'python', SCRIPTS_DIR.join('filter_bounding_box.py'),
            OKCOORDS[:lng0], OKCOORDS[:lat0], OKCOORDS[:lng1], OKCOORDS[:lat1], '-',
            '>', ok_filename
          ]
    sh cmd.join(' ')
  end

end



namespace :fetch  do
  desc "helper task to fetch a single month's worth of data and save it"
  task :yearmonth, [:yearmonth] do |t, args|
    ym = args[:yearmonth]
    cmd = Shellwords.join(['python',
                           SCRIPTS_DIR.join('fetch_month_from_archive.py'),
                           ym])

    Shell.new.system(cmd) > FETCHED_DIR.join(ym + '.csv').to_s
  end


  # All the files to fetch
  ALL_YEAR_MONTHS.each do |ym|
    destname = FETCHED_DIR.join("#{ym}.csv").to_s
    file destname do
      Rake::Task['fetch:yearmonth'].execute(:yearmonth => ym)
    end
  end
end

