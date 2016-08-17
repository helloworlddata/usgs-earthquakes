require 'date'
require 'pathname'
require 'active_support/all'

DATA_DIR = Pathname 'data'
WRANGLE_DIR = Pathname 'wrangle'
SCRIPTS_DIR = WRANGLE_DIR.join('scripts')
FETCHED_DIR = WRANGLE_DIR.join('corral', 'fetched')
COLLATED_DIR = WRANGLE_DIR.join('corral', 'collated')

START_DATE = DateTime.new(1960, 1)
END_DATE = DateTime.now()




task :default => [:setup]

task :setup, :fetch do
    [DATA_DIR, SCRIPTS_DIR, FETCHED_DIR, COLLATED_DIR].each{|p| p.mkpath}
end

namespace :fetch do
    scriptname = SCRIPTS_DIR.join('fetch_archives.py')
    task :yearmonth, [:yearmonth] do |t, args|
        system "python #{scriptname} #{args[:yearmonth]}"
    end

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


namespace :collate do
    # decade is string like '1990'
    task :decade, [:decade] do |t, args|
        startyr = args[:decade].to_i / 10 * 10
        endyr = startyr + 10
        sh ["python",
            SCRIPTS_DIR.join('collate_time_period.py').to_s,
           "#{startyr} #{endyr}",
           ">",
           COLLATED_DIR.join("decade-#{startyr}.csv").to_s].join(' ')

    end
end

# Packaged files
# decade files
(1960..2000).step(10).each do |decade|
    srcname = COLLATED_DIR.join "decade-#{decade}.csv"
    destname = DATA_DIR.join("usgs-earthquakes-decade-#{decade}.csv").to_s
    # simple copy and renaming
    file destname => [srcname] do
        sh "cp #{srcname} #{destname}"
    end
end




# Collated files
(1960..2000).step(10).each do |decade|
    srcnames = (1..12).map{|m| FETCHED_DIR.join "#{decade}-#{"%02d" % m}.csv"}
    destname = COLLATED_DIR.join("decade-#{decade}.csv").to_s

    file destname => srcnames do
        Rake::Task['collate:decade'].execute(:decade => decade)
    end
end


# Fetched files
START_DATE.upto(END_DATE).map{|d| d.strftime('%Y-%m')}.uniq().each do |ym|
    destname = FETCHED_DIR.join("#{ym}.csv").to_s
    file destname do
        Rake::Task['fetch:yearmonth'].execute(:yearmonth => ym)
    end
end


