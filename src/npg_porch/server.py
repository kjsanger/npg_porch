# Copyright (C) 2021, 2022 Genome Research Ltd.
#
# Author: Kieron Taylor kt19@sanger.ac.uk
# Author: Marina Gourtovaia mg8@sanger.ac.uk
#
# This file is part of npg_porch
#
# npg_porch is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from npg_porch.endpoints import pipelines, tasks

#https://fastapi.tiangolo.com/tutorial/bigger-applications/
#https://fastapi.tiangolo.com/tutorial/metadata

tags_metadata = [
    {
        "name": "pipelines",
        "description": "Manage pipelines.",
    },
    {
        "name": "index",
        "description": "Links to documentation.",
    },
]


app = FastAPI(
    title = "Pipeline Orchestration (POrch)",
    openapi_url = "/api/v1/openapi.json",
    openapi_tags = tags_metadata,
)
app.include_router(pipelines.router)
app.include_router(tasks.router)

@app.get(
    "/",
    response_class=HTMLResponse,
    tags=["index"],
    summary="Web page with links to OpenAPI documentation."
)
async def root():
    return """
    <html>
        <head>
            <title>About Pipeline Orchestration</title>
        </head>
        <body>
            <h1>JSON API for Pipeline Orchestration</h1>
            <p><a href="/docs">docs</a></p>
            <p><a href="/redoc">redoc</a></p>
            <p><a href="/api/v1/openapi.json">OpenAPI JSON Schema</a></p>
        </body>
    </html>
    """
