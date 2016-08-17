require 'date'
require 'pathname'

DATA_DIR = Pathname 'data'
WRANGLE_DIR = Pathname 'wrangle'
SCRIPTS_DIR = WRANGLE_DIR.join('scripts')
FETCHED_DIR = WRANGLE_DIR.join('corral', 'fetched')
COLLATED_DIR = WRANGLE_DIR.join('corral', 'collated')

START_DATE = DateTime.new(1960, 1)
END_DATE = DateTime.now()
ALL_YEAR_MONTHS = START_DATE.upto(END_DATE).map{|d| d.strftime('%Y-%m')}.uniq()

PACKAGES = {
  :decades => (1960..2000).step(10),
  :periods => [(2010..2014),],        # too big for a decade
  :years => 2015..END_DATE.year       # each of these years are too big for a single file
}


task :default => [:setup]

desc 'setup the directories'
task :setup do
  puts "Creating directories"
  [DATA_DIR, SCRIPTS_DIR, FETCHED_DIR, COLLATED_DIR].each{|p| p.mkpath}
end


# Packaged files
# decade files

namespace :package do
  PACKAGES[:decades].each do |decade|
    srcname = COLLATED_DIR.join "decade-#{decade}.csv"
    destname = DATA_DIR.join("usgs-earthquakes-decade-#{decade}.csv").to_s
    # simple copy and renaming
    desc "package decade file #{decade}"
    file destname => srcname do
      sh "cp #{srcname} #{destname}"
    end
  end

  PACKAGES[:periods].each do |period|
    px = period.first
    py = period.last
    srcname = COLLATED_DIR.join "#{px}-through-#{py}.csv"
    destname = DATA_DIR.join "usgs-earthquakes-#{px}-through-#{py}.csv"
    desc 'package px-through-py.csv'
    file destname => srcname do
      sh "cp #{srcname} #{destname}"
    end
  end

  PACKAGES[:years].each do |year|
    srcname = COLLATED_DIR.join "#{year}.csv"
    destname = DATA_DIR.join "usgs-earthquakes-#{year}.csv"
    desc "package single year #{year}"
    file destname => srcname do
      sh "cp #{srcname} #{destname}"
    end
  end

  desc "package the last month and year file"
  task :recent
end


namespace :collate do
  # Collated files
  DECADES_TO_PACKAGE.each do |decade|
    # e.g. 1970-01 to 1979-12
    yms = DateTime.new(decade, 1).upto(DateTime.new(decade + 9, 12)).map{|d| d.strftime('%Y-%m')}.uniq()
    srcnames = yms.map{|x| FETCHED_DIR.join "#{x}.csv"}
    destname = COLLATED_DIR.join("decade-#{decade}.csv").to_s

    file destname => srcnames do
      Rake::Task['collate:decade'].execute(:decade => decade)
    end
  end


  # collated periods
  PERIODS_TO_PACKAGE.each do |period|
    px = period.first
    py = period.last
    pyms = (px..py).map{ |y| (1..12).map{|m| "#{y}-#{"%02d" % m}"}}.flatten()
    srcnames = pyms.map{ |ym| FETCHED_DIR.join "#{ym}.csv"}
    collated_through_filename = COLLATED_DIR.join "#{px}-through-#{py}.csv"
    file collated_through_filename => srcnames do
      sh ["python",
            SCRIPTS_DIR.join('collate_time_period.py').to_s,
            px, py+1,
            ">",
            collated_through_filename
          ].join(' ')
    end
  end


  # decade is string like '1990'
  task :decade, [:decade] do |t, args|
    startyr = args[:decade].to_i / 10 * 10
    endyr = startyr + 10
    sh ["python",
          SCRIPTS_DIR.join('collate_time_period.py').to_s,
          "#{startyr} #{endyr}",
          ">",
          COLLATED_DIR.join("decade-#{startyr}.csv").to_s
        ].join(' ')
  end

  # year is something like 1992
  task :year, [:year] do |t, args|
    sh ["python",
          SCRIPTS_DIR.join('collate_time_period.py').to_s,
          "#{year} #{year}",
          ">",
          COLLATED_DIR.join("#{year}.csv").to_s
       ].join(' ')
  end

end


namespace :fetch  do
  # Fetched files
  ALL_YEAR_MONTHS.each do |ym|
    destname = FETCHED_DIR.join("#{ym}.csv").to_s
    file destname do
      Rake::Task['fetch:yearmonth'].execute(:yearmonth => ym)
    end
  end

  desc "helper task to fetch a single month's worth of data and save it"
  task :yearmonth, [:yearmonth] do |t, args|
    scriptname = SCRIPTS_DIR.join('fetch_archives.py')
    system "python #{scriptname} #{args[:yearmonth]}"
  end

  desc "helper task that wraps around fetch:yearmonth"
  task :since, [:startdate, :enddate] do |t, args|
    args.with_defaults(:enddate => END_DATE.strftime('%Y-%m'))
    startdate = DateTime.strptime(args[:startdate], '%Y-%m')
    enddate =  DateTime.strptime(args[:enddate], '%Y-%m')
    monthdates = startdate.upto(enddate).map{|d| d.strftime('%Y-%m')}.uniq()
    monthdates.each do |md|
      Rake::Task["fetch:yearmonth"].execute(:yearmonth => md)
    end
  end
end

