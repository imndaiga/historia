# miminani

### miminani is a Kiswahili portmanteau derived from **_"Mimi Nani?"_**. A question that asks **_"Who Am I?"_**

**miminani** is a web app designed and developed to be a global personal addressing system. It is built on top of a social graph that computatively populates user family trees and generational lineages using their social network connections (only facebook support is currently under consideration).

Submitted data can used for statistical research into social genealogical structures. The project can also be extended to enable for varied social network analyses e.g. an Electronic Medical Record ([EMR](https://en.wikipedia.org/wiki/Electronic_health_record)) System.

####Feature pipeline:
- [ ] Integrate with [Auth0](https://auth0.com/) for frictionless sign-up and registration. :tada:
- [ ] Powered by restful APIs in the backend. :fist:
- [ ] Progressive web app client on the frontend. :construction:
- [ ] Integrate social graph search strategies with [networkx](https://networkx.github.io/). :tada:
- [ ] [Docker](https://www.docker.com/) powered development and deployment workflow.
- [ ] Integrate with [Facebook's Social Graph API](https://developers.facebook.com/docs/graph-api).
- [ ] Permissions-based modification of social graph.
- [ ] Generate social graph visualisations with [sigmajs](http://sigmajs.org/). :fist:

Key | Description
--- | -----------
:construction: | _currently under development_
:fist:         | _progressive development_
:tada:      | _feature complete_

## Usage
Developer usage is simple enough and powered by docker. Currently, this app is client rendered with the [VueJS](https://vuejs.org/) framework, with the backend APIs powered by [Flask](http://flask.pocoo.org/). The only requirement for any host developer environment (Windows, Linux or MacOS) is to have a running installation of [docker](http://www.docker.com/).

Instructions on how to locally run, develop or test your own app instance coming soon! :hourglass_flowing_sand:

### Changelog
#### Version 0.1
- Database models based on graph nodes and edges.
- Welcome page with passwordless authentication.
- Transactional Mail functionality.
- backend testing suite.

#### Version 0.2
 - VueJS frontend client.
 - Restful API powered backend.

#### Version 0.3
- Form validations implemented.
- Graph rendering with sigmaJS.
- Mock data capability in backend.