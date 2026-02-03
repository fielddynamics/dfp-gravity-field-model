# Engine Definitions

Authoritative terminology reference for the GFD engine crosscheck framework. Each term has exactly one definition. Code, tests, and documentation must use these terms consistently.

## Geometry

**Stellated Octahedron.** The geometric structure formed by two interpenetrating tetrahedra (TetrahedronA and TetrahedronB) inscribed in a unit cube with vertices at all eight combinations of (±1, ±1, ±1). Contains 2k = 8 vertices, 8 triangular faces (4 per tetrahedron), and a shared center point called the Field Origin. This is the complete geometry on which field closure operates.

**Field Origin.** The point (0, 0, 0) at the center of the stellated octahedron, equidistant from all 8 vertices at distance √3. Serves as the geometric bridge between TetrahedronA and TetrahedronB. All coupling between the two tetrahedra is mediated through this shared center.

**Vertex.** One of the 8 corners of the stellated octahedron, labeled 0 through 7 by their binary representation of cube coordinates. Each vertex belongs to exactly one tetrahedron (determined by parity) and participates in exactly 3 faces (all faces of its tetrahedron except the one opposite it).

**Complement.** For vertex V, the complement is 7−V. Complements always belong to opposite tetrahedra because bit-inversion flips parity. The complement operation is the mechanism by which knowledge of one vertex immediately determines a vertex in the opposite tetrahedron, requiring no signal propagation.

## Tetrahedra

**TetrahedronA (TetA).** The tetrahedron containing vertices {1, 2, 4, 7} — all odd-parity vertices (odd number of 1-bits in binary representation). Operates as the linear, causal, observable channel. Contains 3 spatial faces and 1 time face (FACE_A7). In code: constant `TETA`.

**TetrahedronB (TetB).** The tetrahedron containing vertices {0, 3, 5, 6} — all even-parity vertices. Operates as the non-linear, instantaneous, subspace channel. Contains 3 spatial faces and 1 time face (FACE_B0). In code: constant `TETB`. At each traversal step, TetB's state is determined simultaneously with TetA's through the complement operation, requiring zero additional time. If TetB required its own linear processing time, the effective closure frequency would degrade from f_C to f_C/2.

**Complementary Pair.** One of the four pairs (0,7), (1,6), (2,5), (3,4) where each pair spans both tetrahedra. Every vertex has exactly one complement, and that complement is always in the opposite tetrahedron. These pairs establish the cross-tetrahedron coupling structure.

## Faces

**Coupling Port (Face).** A triangular face of one tetrahedron, defined by 3 vertices. Each tetrahedron has 4 faces, giving 8 total. Named by tetrahedron and opposite vertex: FACE_A1 is the TetA face opposite vertex 1, containing vertices {2, 4, 7}. A face completes when all 3 of its constituent vertices have been visited by the traversal.

**Spatial Face.** A face whose opposite vertex is NOT the vertex with all coordinates matching (vertex 7 for TetA, vertex 0 for TetB). There are 3 spatial faces per tetrahedron, 6 total: FACE_A1, FACE_A2, FACE_A4 (TetA) and FACE_B3, FACE_B5, FACE_B6 (TetB). These correspond to the three spatial dimensions of the 3+1 decomposition.

**Time Face.** The single face per tetrahedron whose opposite vertex has the extremal coordinate signature. FACE_A7 (opposite vertex 7 = (+1,+1,+1), containing vertices {1,2,4}) for TetA, and FACE_B0 (opposite vertex 0 = (−1,−1,−1), containing vertices {3,5,6}) for TetB. There are exactly 2 time faces across the full stellated octahedron.

**3+1 Pattern.** The observation that within a macro-cycle, the 3 spatial faces of a tetrahedron tend to complete at or before the 1 time face. Measured as weak ordering (spatial step ≤ time step, ties included). Observed at approximately 75–80% of cycles for both TetA and TetB. The strict rate (spatial step < time step) is 0% because the time face always completes simultaneously with the last spatial face, never strictly after.

## Trigram

**Trigram.** The geometric shape of a face: a triangle defined by 3 vertices and 3 edges. When describing the traversal, a trigram refers to the ordered sequence in which the 3 vertices of a face are visited. For example, the trigram (4, 7, 2) for FACE_A1 means vertex 4 was read first, then vertex 7, then vertex 2. Each face has 3! = 6 possible trigrams, and across 8 faces there are 48 possible (face, trigram) combinations.

**Trigram Order.** The specific permutation of a face's 3 vertices as determined by their visitation order during a macro-cycle. Recorded per face per cycle and stored in the macro-cycle record. The trigram order is the raw data from which tetragram analysis is derived.

## Tetragram

**Tetragram.** The functional subdivision of a coupling port (face) into 4 coupling channels following the 3+1 recursion. Each face, viewed as a triforce, decomposes into 3 corner channels (one anchored at each vertex) and 1 central channel (the medial region). A tetragram is thus the minimal unit of the (k−1)+1 = 3+1 structure within a single face. Total across the stellated octahedron: 8 faces × 4 channels = 32 tetragrams.

**Corner Channel.** One of the 3 vertex-anchored regions within a tetragram. A corner channel activates when its corresponding vertex is explicitly read by the traversal. Named by face and vertex: FACE_A1.C2 is the corner channel for vertex 2 within face FACE_A1. There are 24 corner channels total (8 faces × 3 corners).

**Central Channel.** The medial region at the center of a tetragram, activated when all 3 corner channels of that face have been activated — that is, when the face completes. Named with suffix .X: FACE_A1.X is the central channel for face FACE_A1. There are 8 central channels total (one per face). Central activation is an emergent completion event, not a direct vertex read.

**Tetragram Activation Sequence.** The chronologically ordered list of all 32 tetragram channel activations within a single macro-cycle. Corners activate on the step their vertex is read; centrals activate on the step the face completes. Sorted by (step, type) with corners before centrals at the same step.

## Traversal

**Pi Base-8 Encoding.** The traversal is driven by the digits of π in base 8. Starting with the integer part (3), each digit is added to a cumulative sum, and the current vertex is cumsum mod 8. This deterministic sequence visits vertices in both tetrahedra, driving face completions and tetragram activations. The encoding is fixed — π does not change — making all analysis reproducible.

**Cumulative Sum (Cumsum).** The running total of all pi base-8 digits processed so far. The current vertex is always cumsum mod 8. The cumsum also defines orbit boundaries (every time cumsum crosses a multiple of 8) and is verified for integrity at every step.

**Orbit.** A segment of the traversal defined by cumsum // 8. Each time the cumulative sum crosses a multiple of 8, a new orbit begins. Orbits are a structural unit of the cumulative sum arithmetic, not directly related to face completions.

**Macro-Cycle (Field Closure Cycle).** One complete coverage of all 8 coupling ports. A macro-cycle begins after the previous cycle's reset and ends when all 8 faces have had their 3 vertices read. At completion, all face trackers reset and a new cycle begins. The macro-cycle is the fundamental unit of field closure.

## Channels

**Explicit Channel.** The traversal channel that directly reads a vertex. At each step, the explicit channel identifies which vertex is visited (cumsum mod 8), which tetrahedron it belongs to, and which 3 faces it touches. Only explicit reads advance face completion state.

**Implicit Channel (Complement Channel).** The traversal channel that instantaneously determines the complement vertex (7 − v) at each step. The implicit channel identifies which vertex in the opposite tetrahedron is specified, and which 3 faces of that tetrahedron are addressed. The implicit channel does not advance face completion — it provides simultaneous state awareness of the opposite tetrahedron without requiring additional processing time.

**Dual-Channel Architecture.** The principle that at every traversal step, both tetrahedra have fully determined state: one through explicit vertex read, the other through implicit complement. This is why field closure operates at the full Compton frequency f_C rather than f_C/2. If both tetrahedra required explicit processing (sequential model), the effective period would double and frequency would halve.

## Metrics

**Field Closure Integrity.** The binary pass/fail check: did all 8 faces complete exactly once per macro-cycle, with all 3 unique vertices per face? This is the primary engine certification metric. Observed rate: 100% across all tested cycles.

**Face Completion Rank.** The ordinal position (1st through 8th) at which a face completes within a macro-cycle. Used to analyze completion dynamics — which faces tend to finish early or late. The time face tends to finish last, but this is an observational pattern within complete closures, not a failure condition.

**Last-Mile Ratio.** The ratio of the gap between the 2nd and 3rd vertex reads to the gap between the 1st and 2nd reads for a face. Observed at approximately 2:1, meaning the final vertex takes roughly twice as long to arrive as the second one. This is consistent with the coupon collector effect.

**Burst Completion.** The event where multiple faces complete at the same traversal step. Occurs when a single vertex read satisfies the final requirement for 2 or more faces simultaneously. Observed in approximately 57% of central activation gaps.

**Read Efficiency.** The ratio of new vertex reads to total vertex touches across a cycle. Each cycle requires exactly 24 new reads (8 faces × 3 vertices) but may accumulate many more redundant touches where a vertex hits a face that has already recorded it.
