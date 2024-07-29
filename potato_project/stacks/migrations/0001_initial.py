from django.db import migrations

def add_initial_stacks(apps, schema_editor):
    Stack = apps.get_model('stacks', 'Stack')
    stacks = [
        # 프로그래밍 언어
        "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "Ruby", "Go", "Rust", "Swift",
        "Kotlin", "PHP", "Scala", "R", "Dart", "Lua", "Haskell", "Erlang", "Clojure", "F#",
        
        # 백엔드 프레임워크
        "Django", "Flask", "FastAPI", "Spring Boot", "Express.js", "Ruby on Rails", "ASP.NET Core",
        "Laravel", "Symfony", "Phoenix", "Gin", "Echo", "Ktor", "Micronaut", "Quarkus", "NestJS",
        "Strapi", "Koa.js", "Fastify", "Sails.js",
        
        # 프론트엔드 프레임워크/라이브러리
        "React", "Vue.js", "Angular", "Svelte", "Ember.js", "Backbone.js", "jQuery", "Preact",
        "Solid.js", "Alpine.js", "Lit", "Stimulus", "Meteor", "Next.js", "Nuxt.js", "Gatsby",
        "Gridsome", "Eleventy", "Astro", "Remix",
        
        # 모바일 개발
        "React Native", "Flutter", "Xamarin", "Ionic", "PhoneGap", "Cordova", "NativeScript",
        "Kivy", "SwiftUI", "Jetpack Compose", "Unity",
        
        # 데이터베이스
        "PostgreSQL", "MySQL", "MongoDB", "SQLite", "Redis", "Cassandra", "Couchbase", "Oracle",
        "Microsoft SQL Server", "MariaDB", "Elasticsearch", "Neo4j", "InfluxDB", "DynamoDB",
        "Firestore", "Realm", "CockroachDB", "TimescaleDB", "RethinkDB", "ArangoDB",
        
        # 클라우드 플랫폼
        "AWS", "Google Cloud Platform", "Microsoft Azure", "Heroku", "DigitalOcean", "Linode",
        "Vultr", "IBM Cloud", "Oracle Cloud", "Alibaba Cloud",
        
        # DevOps 및 인프라
        "Docker", "Kubernetes", "Jenkins", "GitLab CI/CD", "Travis CI", "CircleCI", "Ansible",
        "Terraform", "Puppet", "Chef", "Vagrant", "Prometheus", "Grafana", "ELK Stack", "Nagios", "Zabbix",
        
        # 버전 관리
        "Git", "Mercurial", "SVN",
        
        # API 및 통신
        "REST API", "GraphQL", "gRPC", "WebSocket", "RabbitMQ", "Apache Kafka", "MQTT", "ZeroMQ",
        
        # 프론트엔드 도구
        "Webpack", "Babel", "Sass", "Less", "PostCSS", "Gulp", "Grunt", "Parcel", "Rollup", "Vite",
        
        # 테스팅
        "Jest", "Mocha", "Jasmine", "Selenium", "Cypress", "Puppeteer", "JUnit", "TestNG", "PyTest", "RSpec"
    ]
    for stack in stacks:
        Stack.objects.create(name=stack)

class Migration(migrations.Migration):

    dependencies = [
        ('your_app_name', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_initial_stacks),
    ]