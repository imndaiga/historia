# historia

**historia** is a historical population archive. It is built on top of a social graph that computatively populates familial hierarchies from user-inputted data.

Submitted data can used for statistical research into social genealogical structures. The project can also be extended to enable for varied social network analyses e.g. an Electronic Medical Record ([EMR](https://en.wikipedia.org/wiki/Electronic_health_record)) System.

#### Feature pipeline:
- :o: [GraphQL-powered](http://graphql.org/) APIs.
- :o: Implement a full-text search engine.
- :red_circle: Integrate with [Facebook's Social Graph API](https://developers.facebook.com/docs/graph-api).
- :red_circle: Permissions-based modification of social graph.

Key | Description
--- | -----------
:o:   | _Under development_
:red_circle: | _PRs welcome_

#### Changelog

##### Version 0.5
- NuxtJS dropped in favour of VueJS's webpack template.

##### Version 0.4.5
- Client powered by [NuxtJS.](https://nuxtjs.org/)
- Docker/[PostgreSQL](https://www.postgresql.org/) powered database.

##### Version 0.4
- Frontend served with [express.js.](http://expressjs.com/)
- Editable table entries and relationships.
- Cleaner UI and UX.
- Refactored code.

##### Version 0.3
- Form validations implemented.
- Graph rendering with sigmaJS.
- Mock data capability in backend.

##### Version 0.2
 - VueJS frontend client.
 - Restful API powered backend.

##### Version 0.1
- Database models based on graph nodes and edges.
- Welcome page with passwordless authentication.
- Transactional Mail functionality.
- Backend testing suite.