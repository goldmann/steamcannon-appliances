def boxgrinder_build(options)
  if options[:delivery].to_s == 'ami'
    options[:delivery_config] ||= { }
    options[:delivery_config][:region] ||= ENV['REGION']
    options[:delivery_config][:bucket] ||= "#{ENV['BUCKET_PREFIX']}-#{ENV['REGION']}" if ENV['BUCKET_PREFIX']
  end
  cmd = "boxgrinder build appliances/#{options[:appliance]}.appl -p #{options[:platform]}"
  cmd << " -d #{options[:delivery]}" if options[:delivery]
  cmd << " --delivery-config #{hash_to_cli_config(options[:delivery_config])}" if options[:delivery_config]
  sh cmd
end

def hash_to_cli_config(hash)
  cfg = []
  hash.each { |k,v| cfg << "#{k}:#{v}"}
  cfg.join(" ")
end

def determine_value(file_path, key)
  File.open( file_path ) do |f|
    f.each_line do |line|
      if ( line =~ %r(^\s*%define\s*#{key}\s*([^\s]+)) )
        return $1
      end
    end
  end
  nil
end

def scribble_config(plugin, options = {})
  copy( boxgrinder_config_file(plugin), boxgrinder_config_file_bak(plugin) )
  config = YAML.load_file( boxgrinder_config_file(plugin) )
  config.merge!(options)
  File.open( boxgrinder_config_file(plugin), 'w' ) do |out|
    YAML.dump( config, out )
  end
end

def restore_config(plugin)
  move( boxgrinder_config_file_bak(plugin), boxgrinder_config_file(plugin) )
end

def scribble_s3
  copy( boxgrinder_config_file('s3'), boxgrinder_config_file_bak('s3') )
  config = YAML.load_file( boxgrinder_config_file('s3') )
  config['bucket'] = config['bucket'] + "-" + rand(10000).to_s
  File.open( boxgrinder_config_file('s3'), 'w' ) do |out|
    YAML.dump( config, out )
  end
end

def restore_s3
  move( boxgrinder_config_file_bak('s3'), boxgrinder_config_file('s3') )
end

def boxgrinder_config_file(plugin)
  "#{ENV['HOME']}/.boxgrinder/plugins/#{plugin}"
end

def boxgrinder_config_file_bak(plugin)
  boxgrinder_config_file(plugin) + ".bak"
end

class BuildVersion
  include Singleton

  attr_accessor :steamcannon, :steamcannon_agent, :torquebox, :deltacloud, :torquebox_rpm

  def initialize()
    @steamcannon       = nil
    @steamcannon_agent = nil
    @torquebox         = nil
    @deltacloud        = '0.1.1.3'
    @torquebox_rpm     = '1.0.0.RC1.SNAPSHOT'

    torquebox_versions = {}
    [
      './specs/torquebox-deployers.spec',
      './specs/torquebox-cloud-profiles-deployers.spec',
      '../torquebox-rpm/specs/torquebox-rubygems.spec',
    ].each do |spec|
      torquebox_versions[spec] = determine_value( spec, 'torquebox_build_number' )
    end
    if ( torquebox_versions.values.uniq.size == 1 )
      @torquebox = torquebox_versions.values.uniq.first
    else
      puts "TorqueBox build number mismatch!"
      torquebox_versions.each do |spec, ver|
        puts "  #{ver} - #{spec}"
      end
      fail( "TorqueBox build number mismatch" )
    end
    @steamcannon = determine_value( './specs/steamcannon.spec', 'steamcannon_version' )
    @steamcannon_agent = determine_value( './specs/steamcannon-agent.spec', 'steamcannon_agent_version' )
  end

end

