import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('2020 CNCF Annual Report', 'The Cloud Native Computing Foundation (CNCF) annual report for 2020 is now available. The report highlights the growth of the community, events, projects, and more, over the past year.')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('KubeCon + CloudNativeCon 2021', 'The Cloud Native Computing Foundation flagship conference gathers leading technologists from leading open source and cloud native communities to further the education and advancement of cloud native computing.')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Kubernetes v1.20 Release Notes', 'Kubernetes is an open source container orchestration engine for automating deployment, scaling, and management of containerized applications. The open source project is hosted by the Cloud Native Computing Foundation (CNCF).')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('CNCF Cloud Native Interactive Landscape', 'This landscape is intended as a map through the previously uncharted terrain of cloud native technologies. There are many routes to deploying a cloud native application, with CNCF Projects representing a particularly well-traveled path.')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('CNCF Cloud Native Definition v1.0', 'Cloud native technologies empower organizations to build and run scalable applications in modern, dynamic environments such as public, private, and hybrid clouds. Containers, service meshes, microservices, immutable infrastructure, and declarative APIs exemplify this approach. \nThese techniques enable loosely coupled systems that are resilient, manageable, and observable. Combined with robust automation, they allow engineers to make high-impact changes frequently and predictably with minimal toil.\nThe Cloud Native Computing Foundation seeks to drive adoption of this paradigm by fostering and sustaining an ecosystem of open source, vendor-neutral projects. We democratize state-of-the-art patterns to make these innovations accessible for everyone.')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Kubernetes Certification', 'CNCF, along with the Linux Foundation, have created certification programs for Kubernetes as well as training for CNCF projects Prometheus and Fluentd.')
            )

connection.commit()
connection.close()
