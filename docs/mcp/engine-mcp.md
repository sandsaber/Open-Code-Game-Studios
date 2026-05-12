# Engine MCP Integration

MCP integrations are optional engine adapters. They let AI tools interact with a
running game editor, but they also expand the tool surface that can modify a
project. Enable only the MCP server for the engine selected in
`.claude/docs/technical-preferences.md`.

## Default Recommendations

| Engine | Recommended MCP | Why |
|--------|-----------------|-----|
| Unity | `CoplayDev/unity-mcp` | Active MIT project, Unity package workflow, broad editor tools, HTTP and stdio options. |
| Godot | `Coding-Solo/godot-mcp` | Free MIT project, npm-based setup, good default for launch/run/debug/project inspection. |
| Godot advanced | `youichi-uda/godot-mcp-pro` | Paid server package with deeper editor integration and many tools; use `--minimal` or CLI for OpenCode/local models. |
| Unreal Engine | `chongdashu/unreal-mcp` | Experimental MIT integration for UE 5.5+, with C++ editor plugin plus Python MCP server. |

## Safety Rules

- Treat MCP as an editor automation layer, not a replacement for source control.
- Enable only one engine MCP server per project unless there is a specific reason.
- Prefer read-only inspection first: project info, scene tree, console output, validation.
- Ask for approval before using MCP tools that create, edit, delete, import, build, or run long tasks.
- Do not commit generated editor changes until they have been reviewed in the normal workflow.
- Keep local paths, ports, API keys, and machine-specific settings out of committed files.

## OpenCode Usage

OpenCode supports project-level MCP configuration through `opencode.json`. This
repository keeps `opencode.json` with an empty `mcp` block by default to avoid
starting editor integrations accidentally.

To enable an engine MCP in OpenCode:

1. Choose the engine MCP below.
2. Copy the matching snippet from `.opencode/mcp-examples/`.
3. Merge it into `opencode.json` under the `mcp` key.
4. Restart OpenCode from the project root.
5. Run `/token-optimize [engine task]` before broad editor automation.

## Unity: CoplayDev/unity-mcp

Use for Unity projects when the Unity Editor should be inspectable or controllable
from the AI session.

Recommended setup:

1. Install the Unity package from the Git URL:

   ```text
   https://github.com/CoplayDev/unity-mcp.git?path=/MCPForUnity#main
   ```

2. In Unity, open `Window > MCP for Unity` and start the server.
3. Use HTTP mode for local editor sessions when available:

   ```json
   {
     "mcp": {
       "unityMCP": {
         "url": "http://localhost:8080/mcp"
       }
     }
   }
   ```

4. Use stdio mode when the client or environment requires process-based MCP.

Best fit:

- Scene and asset management
- Editor state inspection
- Console reading and test running
- Unity API verification through MCP tools

## Godot Default: Coding-Solo/godot-mcp

Use this as the default Godot MCP path. It is free, simple to install through
`npx`, and covers the common loop: launch editor, run project, capture debug
output, inspect project structure, and perform basic scene operations.

Generic MCP config:

```json
{
  "mcp": {
    "godot": {
      "command": "npx",
      "args": ["@coding-solo/godot-mcp"],
      "env": {
        "GODOT_PATH": "/path/to/godot",
        "DEBUG": "true"
      }
    }
  }
}
```

Best fit:

- Free/open-source default
- Running Godot projects from an AI session
- Debug output capture
- Basic scene and project operations

## Godot Advanced: godot-mcp-pro

Use Godot MCP Pro only when the project needs deeper editor automation and the
team accepts the paid server package. The public repository contains the Godot
addon, but the Node.js MCP server is distributed in the paid package.

For OpenCode and local models, prefer the smaller tool modes:

```json
{
  "mcp": {
    "godot-mcp-pro": {
      "command": "node",
      "args": ["/path/to/server/build/index.js", "--minimal"],
      "env": {
        "GODOT_MCP_PORT": "6505"
      }
    }
  }
}
```

Best fit:

- Runtime inspection
- UI and input simulation
- Profiling and screenshots
- Batch scene/refactor operations
- Teams that want editor-integrated UndoRedo support

## Unreal Engine: chongdashu/unreal-mcp

Use for Unreal Engine projects that need AI-assisted editor automation. Treat it
as experimental: the upstream project explicitly warns that APIs and behavior may
change and production use is not recommended.

Basic shape:

1. Copy the `UnrealMCP` plugin into the project's `Plugins/` directory.
2. Enable it in the Unreal Editor and rebuild the project.
3. Run the Python MCP server with `uv`.
4. Configure the MCP client:

```json
{
  "mcp": {
    "unrealMCP": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/unreal-mcp/Python",
        "run",
        "unreal_mcp_server.py"
      ]
    }
  }
}
```

Best fit:

- Actor creation and transforms
- Blueprint class and component automation
- Editor viewport control
- Experimental UE 5.5+ workflows

## Project Decision Record

When enabling MCP for a real game project, record the decision in either:

- `.claude/docs/technical-preferences.md` under Engine MCP Integration
- An ADR if the MCP affects build, editor automation, CI, or team workflow

Include:

- MCP server name and version/source
- Engine version
- Enabled transport and port
- Allowed tool categories
- Security restrictions
- Rollback plan
