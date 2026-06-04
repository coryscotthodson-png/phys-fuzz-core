use pyo3::prelude::*;

#[pyclass]
pub struct ReactorState {
    #[pyo3(get, set)] pub radius: f64,
    #[pyo3(get, set)] pub velocity: f64,
    #[pyo3(get)] pub breached: bool,
}

#[pymethods]
impl ReactorState {
    #[new]
    fn new(radius: f64, velocity: f64, breached: bool) -> Self {
        ReactorState { radius, velocity, breached }
    }
}

#[pymodule]
fn cavitation_engine(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<ReactorState>()?;
    #[pyfn(m)]
    fn step(state: &mut ReactorState, freq: f64, amp: f64, dt: f64) -> PyResult<bool> {
        if state.breached { return Ok(true); }
        let c_medium = 850.0;
        let r_min = 1e-9;
        let p_internal = amp * (2.0 * std::f64::consts::PI * freq * state.radius).abs();
        let a = -p_internal / (state.radius + 1e-12);
        state.velocity += a * dt;
        state.radius += state.velocity * dt;
        if state.radius.is_nan() || state.velocity.abs() >= c_medium || state.radius <= r_min {
            state.breached = true;
            return Ok(true);
        }
        Ok(false)
    }
    Ok(())
}
