from app.providers.app_provider import app
from database.seeders.user_seeder import UserSeeder


class AppSeeder:
    def run(self):
        with app.app_context():
            seeders = [UserSeeder()]

            for seeder in seeders:
                seeder.run()
