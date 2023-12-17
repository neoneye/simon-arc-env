# Rewards

## Set pixel

```
+1 for a pixel set the 1st time.
+0.5 for a pixel set the 2nd time.
+0.25 for a pixel set the 3rd time.
-0.25 for a pixel set the 4th time.
-0.5 for a pixel set the 5th time.
-1 for a pixel set the 6th time.
-1 when setting a pixel to the same value as it already has.
```


## Set visible area

```
+1 when the visible area is set the 1st time.
+0.5 when the visible area is set the 2nd time.
+0.25 when the visible area is set the 3rd time.
-1 when adjusting area to the same size as it already has.
```

## Moving cursors

```
-1 when moving cursors for too long a distance without setting a pixel.
```

## Submit

Terminate the game when the editor is visible.

Truncate the game when the editor is not visible.

```
-1000 when submitting on a page that is not an editor.
+1 when submitting with the right width.
+1 when submitting with the right height.
+1 when submitting with the right size.
+1 when submitting with the right histogram.
-1 when submitting with the wrong histogram.
+1 when submitting with N pixels that all have been assigned.
-1 when submitting with N pixels that haven't been assigned.
```
