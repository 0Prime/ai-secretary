import * as fs from 'fs';
import * as esbuild from 'esbuild';

const isWatch = process.argv.includes('--watch');

const buildOptions: esbuild.BuildOptions = {
  entryPoints: ['main.ts'],
  bundle: true,
  target: 'es2016',
  outfile: 'main.js',
  external: ['obsidian', 'fs', 'path', 'child_process', 'util'],
  format: 'cjs',
  platform: 'node',
  minify: !isWatch,
  sourcemap: isWatch,
};

if (isWatch) {
  const ctx = await esbuild.context(buildOptions);
  await ctx.watch();
  console.log('Watching for changes...');
} else {
  await esbuild.build(buildOptions);
  console.log('Build complete!');
}
