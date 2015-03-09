# ugh-fields
A simple CMS/Static Site generator based on Dropbox API

Ugh Fields allows a complete CMS to live inside of your Dropbox folder. 

Create a new website by creating a directory under the Ugh Fields App folder within your Dropbox folder.

Under the domain directory, create the templates and url structure under a "templates" subdirectory, add CMS data under a "data" directory, and add public static assets under an "assets" directory.

```
Ugh Fields/
├── anotherdomain.com
└── domain.com
    ├── assets
    │   ├── css
    │   ├── img
    │   └── js
    ├── data
    │   └── projects.xlsx
    └── templates
        ├── about
        ├── index.html
        └── projects
            ├── index.html
            └── __project_id__.html
```

