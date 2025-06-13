# Math Visualizer
An interactive web application that brings mathematical concepts to life through beautiful visualizations. Explore fractals, procedural terrain generation, and complex mathematical structures in real-time.

## [🚀 Live Demo](https://mattfrayser.github.io/math-visualizer/)

## 🌟 Features
### Interactive Visualizations
- Julia Sets: Real-time fractal generation that responds to mouse movement
- Mandelbrot Set: Classic fractal visualization with optimized rendering
- Perlin Noise Terrain: 3D procedural terrain with customizable parameters

### Real-time Interactivity
- Mouse-controlled Julia set parameters
- Live slider controls for Perlin noise generation
- Smooth transitions between different mathematical concepts
- Optimized performance for web deployment

## 📦 Installation & Local Development

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/math-visualizer.git
cd math-visualizer
```
### 2. Install Dependancies
```bash
pip install -r requirements.txt
```
### 3. Run locally
```bash
python main.py
```
### 4. Run on web
```bash
# Will load on localhost:3000
python -m pygbag --build main.py
```

## 🎮 How to Use

### Navigation
Use the bottom navigation buttons to switch between different visualizations

- Julia Sets: Move your mouse around the screen to see how the fractal changes
- Perlin Noise: Adjust the sliders to modify terrain generation parameters
- Mandelbrot: Explore the classic Mandelbrot set fractal

### Controls
Julia Sets
- Mouse Movement: changes the complex parameter c in real-time. The fractal updates dynamically based on your mouse position.

Perlin Noise Terrain
- Scale Slider: Controls the size of terrain features (1-100)
- Octaves Slider: Number of noise layers for detail (1-10)
- Persistence Slider: How much each octave contributes (0.1-1.0)
- Lacunarity Slider: Frequency multiplier between octaves (1.0-3.0)

Mandelbrot Set
- Static visualization of the famous Mandelbrot fractal
- Pre-generated for optimal performance
