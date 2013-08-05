git "/var/www/cinemateca-feed" do
    repository "https://github.com/mtpereira/cinemateca-feed.git"
    action :sync
    user "server"
    group "server"
end
