# Draft: Object mask editor

This is an idea. It's not implemented. I'm considering adding this. Proposed by `Magnum Oops` on lab42 discord.

Some ARC tasks use objects made up of 2 or more colors, that may use connectivity 4 or connectivity 8.
For a human it's easy to see what pixels are glued together into a single object.

Examples of objects manipulations in ARC tasks: 
- Apply gravity to objects, so they fall to the floor. 
- Move objects around, so they align with an edge. 
- Recolor the object.

Having an editor on every page, where it's possible for the agent to draw a mask of what pixels makes up an object.

This will give the agent an object mask to do operations with.

The agent may have to return to the drawing several times to try out different hypothesis.

