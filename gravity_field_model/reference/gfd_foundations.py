# -*- coding: utf-8 -*-
"""
Gravity Field Dynamics: Foundations

A chain of logic establishing WHY gravity must have the structure it does.
This document builds the case from first principles before introducing
the mechanics of how the system works.

The argument proceeds:
1. The overlooked structure at the heart of gravity
2. Gravity is a field (established physics)
3. Is it one field or many? (the critical question)
4. One unified field has fundamental problems
5. Many fields implies topology and packing
6. LIGO confirms the tetrahedral structure
7. Textbooks already describe this (different vocabulary)
8. One tetrahedron is necessary but insufficient
9. Two tetrahedra (stellated octahedron) are required for consistent coupling
10. The field dynamics of this structure explain physics

Usage:
    from gravity_field_model.reference.gfd_foundations import GFD_FOUNDATIONS
"""

# =============================================================================
# GRAVITY FIELD DYNAMICS: FOUNDATIONS
# =============================================================================

GFD_FOUNDATIONS = [
    # =========================================================================
    # PROLOGUE: THE OVERLOOKED STRUCTURE
    # =========================================================================
    {
        "id": "the_overlooked_structure",
        "title": "The Structure Hiding in Plain Sight",
        "section": "Prologue",
        "order": 1,
        "content": (
            "For over forty years, textbook gravitational physics has contained a dual "
            "tetrahedral structure at its mathematical core. The ADM formalism has four "
            "constraints. The tetrad has four legs. Loop Quantum Gravity builds space from "
            "quantum tetrahedra. Regge calculus tiles spacetime with simplices. The number "
            "four appears everywhere, and where there is coupling between metrics, there are "
            "two sets of four. Two tetrahedra. Yet this structure rarely makes it into the "
            "discussion of what gravity actually is.\n\n"
            "Consider an analogy. Imagine if molecular biology had spent decades studying "
            "cell function while treating the nucleus as a minor detail. The equations would "
            "work. The predictions would match experiment. But the six feet of DNA packed into "
            "every nucleus, the information architecture that actually runs the cell, would "
            "remain curiously absent from the conceptual picture. The mathematics would contain "
            "it; the understanding would not.\n\n"
            "Something similar has happened in gravitational physics. The dual tetrahedral "
            "structure is present in the mathematics. It appears in the constraint algebra, in "
            "the vierbein formalism, in the spin network nodes. But when physicists picture "
            "gravity, they picture smooth curvature, not interlocking tetrahedra. When the "
            "equations predicted more gravity than visible matter could explain, the response "
            "was to add invisible matter rather than examine the topology that was already there.\n\n"
            "This document walks through the textbook foundations that lead, step by step, to "
            "the dual tetrahedral structure. Nothing here is new physics. What is new is taking "
            "the structure seriously.\n\n"
            "--- THREE ROUTES TO THE SAME SCALE ---\n\n"
            "Here is what taking the structure seriously produces. Three independent "
            "calculations, using different physics, converge on the same characteristic scale.\n\n"
            "ROUTE 1: ELECTROMAGNETISM\n"
            "The classical electron radius, where EM self-energy equals rest mass:\n\n"
            "    r_e = e^2 / (4 pi epsilon_0 m_e c^2)\n"
            "    r_e = 2.818 fm\n\n"
            "This uses electromagnetism only. No gravity. No cosmology.\n\n"
            "ROUTE 2: GRAVITATIONAL TOPOLOGY\n"
            "If k=4 closure couples gravity to the MOND acceleration scale:\n\n"
            "    r = k x sqrt(G m_e / a_0)\n"
            "    r = 4 x sqrt[(6.67e-11)(9.11e-31) / (1.22e-10)]\n"
            "    r = 2.82 fm\n\n"
            "This uses gravity and cosmology. No electromagnetism.\n\n"
            "ROUTE 3: THE FIELD CLOSURE TEST\n"
            "If k=4 topology is real, the ratio a_0 / (G m_e / r_e^2) should equal k^2 = 16:\n\n"
            "    a_0 / (G m_e / r_e^2) = (1.22e-10) / [(6.67e-11)(9.11e-31) / (2.818e-15)^2]\n"
            "    a_0 / (G m_e / r_e^2) = 15.93\n\n"
            "Predicted: 16. Measured: 15.93. Match: 0.4%.\n\n"
            "Three routes. Three different sets of physics. Same answer: 2.82 femtometers.\n\n"
            "Now, Route 3 deserves a moment. Look at what it actually says. The MOND "
            "acceleration scale divided by the gravitational acceleration at the electron "
            "radius equals k squared. Equals 16. Equals the number of coupling channels in "
            "tetrad gravity (4 legs times 4 legs). That is field closure. That is the "
            "requirement, present in every GR textbook, that gravitational fields must "
            "complete. They cannot have gaps. They cannot leave directions undefined. The "
            "geometry must close.\n\n"
            "Field closure is not exotic physics. It is the most basic requirement of general "
            "relativity. The metric must be non-degenerate. The tetrad must span the tangent "
            "space. The constraints must be satisfied. Every graduate student learns this in "
            "their first GR course. What they do not learn, because no one bothers to "
            "calculate it, is that this simple requirement, fields must close, gives you the "
            "electron scale.\n\n"
            "That is the magic trick. Not new physics. Just taking the old physics seriously "
            "enough to compute what it predicts.\n\n"
            "This is not coincidence. This is the characteristic size of a gravity field unit. "
            "The classical electron radius is not merely an electromagnetic curiosity. It is "
            "the scale at which field closure operates. The electron is the particle whose "
            "mass corresponds to exactly one unit of gravitational field closure.\n\n"
            "The structure was always in the textbooks. The scale was always derivable. What "
            "follows is the complete chain of logic."
        )
    },
    
    # =========================================================================
    # SECTION I: THE STARTING POINT
    # =========================================================================
    {
        "id": "gravity_is_a_field",
        "title": "Gravity Is a Field",
        "section": "The Starting Point",
        "order": 2,
        "content": (
            "General relativity established that gravity is a field, not a force acting at a "
            "distance. Mass and energy curve spacetime geometry, and objects follow geodesics "
            "through that curvature. This is confirmed physics: GPS satellites correct for "
            "gravitational time dilation, LIGO detects ripples in the gravitational field, and "
            "light bends around massive objects exactly as the field equations predict.\n\n"
            "The gravitational field pervades all of space. Every point has a geometry: a local "
            "clock rate, a local length scale, a local curvature. Matter tells spacetime how to "
            "curve; curved spacetime tells matter how to move. This is textbook physics, "
            "established through a century of precision tests.\n\n"
            "The question that follows is not WHETHER gravity is a field, but WHAT KIND of field. "
            "This question determines the structure of gravitational physics. And here, curiously, "
            "the textbooks provide an answer that few physicists discuss at dinner parties."
        )
    },
    {
        "id": "one_or_many",
        "title": "The Critical Question: One Field or Many?",
        "section": "The Starting Point",
        "order": 3,
        "content": (
            "The gravitational field filling the universe presents two possibilities. Is it one "
            "continuous field stretching from here to the cosmic horizon, like a single ocean? "
            "Or is it composed of many discrete units, like water composed of molecules?\n\n"
            "This is not philosophy. It is physics with testable consequences. Each answer leads "
            "to different predictions about how gravity works, how information propagates, and "
            "what happens at cosmic scales.\n\n"
            "The continuous-field picture is intuitive. Smooth curvature, elegant geometry, "
            "Einstein's beautiful equations. It is also, as we shall see, incomplete in ways "
            "that matter. The evidence points toward discrete structure, and that structure has "
            "a specific shape."
        )
    },
    
    # =========================================================================
    # SECTION II: THE PROBLEM WITH ONE FIELD
    # =========================================================================
    {
        "id": "thermodynamic_problem",
        "title": "The Thermodynamic Problem",
        "section": "Problems with One Unified Field",
        "order": 4,
        "content": (
            "A single continuous field stretching across the universe faces a thermodynamic "
            "problem. A field with no internal structure has no mechanism to store, process, or "
            "release information locally. Every disturbance must propagate through the entire "
            "field, affecting everything everywhere.\n\n"
            "Consider what happens when a star forms. Mass concentrates, geometry curves, and "
            "the gravitational field must adjust. In a single unified field, this adjustment "
            "requires global reorganization. The field at the cosmic horizon must somehow "
            "respond to a star forming in a distant galaxy. Information must travel across "
            "10^26 meters, but instantaneous propagation violates causality.\n\n"
            "A continuous field with no substructure provides no mechanism for local processing, "
            "no means to achieve consistency without global coordination. The thermodynamics "
            "requires internal structure. The question is what kind."
        )
    },
    {
        "id": "information_problem",
        "title": "The Information Propagation Problem",
        "section": "Problems with One Unified Field",
        "order": 5,
        "content": (
            "Information in physics must be carried by something. In electromagnetism, photons "
            "carry information. In the strong force, gluons serve this function. What carries "
            "gravitational information?\n\n"
            "If gravity is one unified field with no internal structure, nothing carries "
            "information from one region to another. The field exists, everywhere, all at once. "
            "Yet general relativity requires that gravitational changes propagate at the speed "
            "of light. LIGO confirmed this directly: gravitational waves from black hole mergers "
            "1.3 billion light-years away took 1.3 billion years to reach Earth.\n\n"
            "Waves are disturbances in a medium. For gravitational waves to propagate, there "
            "must be something that can be disturbed, something that can oscillate, something "
            "that can carry the wave from source to detector. The medium need not be mechanical, "
            "but it must have structure. Featureless fields do not wave."
        )
    },
    {
        "id": "constraint_problem",
        "title": "The Constraint Satisfaction Problem",
        "section": "Problems with One Unified Field",
        "order": 6,
        "content": (
            "General relativity requires that geometry be consistent everywhere. The Einstein "
            "field equations must be satisfied at every point. The ADM formalism makes this "
            "explicit: four constraint equations (one Hamiltonian, three momentum) must hold on "
            "every spatial slice. These constraints enforce that the geometry represents a valid "
            "solution to Einstein's equations.\n\n"
            "A constraint is not self-enforcing. Something must satisfy it. What mechanism "
            "ensures that the geometry at point A is consistent with the geometry at point B? "
            "In a single unified field, consistency requires global knowledge. But global "
            "knowledge requires faster-than-light communication, which violates causality.\n\n"
            "The resolution requires structure: a mechanism for local processing that achieves "
            "consistency without global coordination. This mechanism requires discrete field "
            "units that can couple locally to their neighbors. And as we shall see, the "
            "constraints themselves tell us exactly how many coupling directions are needed."
        )
    },
    
    # =========================================================================
    # SECTION III: MANY FIELDS - THE RESOLUTION
    # =========================================================================
    {
        "id": "many_fields_resolution",
        "title": "The Resolution: Gravity Is Many Fields",
        "section": "The Resolution: Many Fields",
        "order": 7,
        "content": (
            "The problems with one unified field share a common resolution: internal structure. "
            "If the gravitational field is composed of many discrete units, each unit can "
            "process locally. Information can propagate from unit to unit. Consistency can be "
            "achieved through local coupling rather than global coordination.\n\n"
            "This resolution follows established physics. Water appears continuous but is "
            "composed of molecules. Sound waves appear smooth but propagate through discrete "
            "atoms. Electromagnetic fields carry energy in quantized packets. The gravitational "
            "field follows the same pattern: continuous appearance emerging from discrete "
            "structure.\n\n"
            "Textbook physics already points to this structure. Loop Quantum Gravity identifies "
            "the tetrahedron as the quantum of space. Regge calculus builds spacetime from "
            "discrete simplices. The tetrad formalism requires four orthonormal vectors at each "
            "point. The discrete structure is present in the mathematics. What follows is "
            "taking it seriously as physics."
        )
    },
    {
        "id": "topology_and_packing",
        "title": "Topology and the Simplex Theorem",
        "section": "The Resolution: Many Fields",
        "order": 8,
        "content": (
            "Once gravity is understood as many discrete field units, the question becomes: how "
            "do they pack together? This is topology, the mathematics of how shapes fit in "
            "space. The answer comes from the simplex theorem, a result so fundamental it is "
            "often unstated.\n\n"
            "The simplex theorem: to enclose a region in d dimensions requires d+1 points. In "
            "one dimension, 2 points bound an interval. In two dimensions, 3 points bound a "
            "triangle. In three dimensions, 4 points bound a tetrahedron. This is geometric "
            "necessity, not convention.\n\n"
            "For the gravitational field in three-dimensional space, each field unit requires 4 "
            "interfaces to form a closed boundary. Fewer than 4 leaves gaps; more than 4 is "
            "redundant. The fundamental unit of gravitational field structure is bounded by "
            "exactly 4 faces. This is the tetrahedron: the minimal solid in three dimensions, "
            "the unique shape that satisfies k=4 closure.\n\n"
            "The number 4 is not chosen. It is forced by geometry."
        )
    },
    
    # =========================================================================
    # SECTION IV: OBSERVATIONAL CONFIRMATION
    # =========================================================================
    {
        "id": "ligo_confirmation",
        "title": "LIGO Confirms k=4 Structure",
        "section": "Observational Confirmation",
        "order": 9,
        "content": (
            "LIGO detected gravitational waves from merging black holes and neutron stars, "
            "confirming that gravity propagates at the speed of light. LIGO also measured "
            "exactly two polarizations for these waves. This measurement, often reported as "
            "confirmation of general relativity, actually reveals the internal structure of "
            "the gravitational field.\n\n"
            "The metric tensor in general relativity has 10 independent components. After "
            "accounting for constraints and gauge freedom, the physical degrees of freedom "
            "equal 10 - 2k, where k is the number of constraint directions. LIGO measured "
            "10 - 2k = 2 polarizations. This determines k = 4.\n\n"
            "This value k=4 appears throughout gravitational physics: 4 constraint equations in "
            "ADM formalism, 4 basis vectors in the tetrad, 4 faces of the quantum tetrahedron in "
            "Loop Quantum Gravity, 4 vertices of the 3-simplex in Regge calculus. LIGO provided "
            "direct observational confirmation of what the mathematics already contained.\n\n"
            "Water molecules have tetrahedral hydrogen bonding. Gravity fields have tetrahedral "
            "closure. Both require 4 coupling directions to form stable configurations in 3D "
            "space. The geometry is the same because the dimensional constraint is the same."
        )
    },
    {
        "id": "wave_structure",
        "title": "Gravitational Waves: The Medium Question",
        "section": "Observational Confirmation",
        "order": 10,
        "content": (
            "When LIGO detects a gravitational wave, what medium supports the wave? Textbooks "
            "state that spacetime geometry itself oscillates. This is correct but raises a "
            "question: geometry is a description, not a substance. What physical structure "
            "carries the oscillation?\n\n"
            "Consider ocean waves. The wave is a pattern of motion in water molecules. The "
            "molecules do not travel with the wave; they oscillate locally while the pattern "
            "propagates horizontally. The wave is a collective phenomenon emerging from the "
            "coordinated motion of discrete units.\n\n"
            "Gravitational waves follow the same pattern. They are geometric disturbances "
            "propagating through discrete field units. Each unit responds to its neighbors, "
            "passing the disturbance along. The wave is the collective response of many field "
            "units to a passing perturbation.\n\n"
            "This explains why gravitational waves propagate at the speed of light: c is the "
            "coupling speed between field units. It is not imposed externally; it emerges from "
            "the structure."
        )
    },
    
    # =========================================================================
    # SECTION V: TEXTBOOK FOUNDATIONS
    # =========================================================================
    {
        "id": "textbook_adm",
        "title": "ADM Formalism: The 4 Constraints",
        "section": "Textbook Foundations",
        "order": 11,
        "content": (
            "The Arnowitt-Deser-Misner formalism recasts Einstein's equations into Hamiltonian "
            "form through 3+1 decomposition: spacetime splits into spatial slices evolving in "
            "time. The result is exactly 4 constraint equations that must be satisfied on every "
            "spatial slice.\n\n"
            "The Hamiltonian constraint H = 0 enforces consistency in the timelike direction. "
            "The three momentum constraints H_i = 0 enforce consistency in each spatial "
            "direction. Together, these 4 equations ensure that the geometry represents a valid "
            "solution to Einstein's field equations.\n\n"
            "This is textbook general relativity (Arnowitt, Deser & Misner 1962; Misner, Thorne "
            "& Wheeler 1973; Alcubierre 2008). Every graduate student learns it. What the "
            "textbooks rarely emphasize is that these 4 constraints define 4 coupling directions, "
            "and 4 directions in 3D space define a tetrahedron.\n\n"
            "The simplex theorem explains WHY there are exactly 4 constraints: d+1 = 4 "
            "directions are required to enforce consistency in d = 3 spatial dimensions plus "
            "time. The constraint structure is the tetrahedral structure."
        )
    },
    {
        "id": "textbook_tetrad",
        "title": "Tetrad Formalism: The 4 Legs",
        "section": "Textbook Foundations",
        "order": 12,
        "content": (
            "The equivalence principle requires that physics be locally special-relativistic at "
            "every point. There must exist a local frame where the metric becomes Minkowski. "
            "The tetrad formalism makes this explicit, and the name itself reveals the structure: "
            "tetrad means four.\n\n"
            "A tetrad consists of 4 orthonormal vector fields: one timelike (e^0) and three "
            "spacelike (e^1, e^2, e^3). The metric is reconstructed from the tetrad: "
            "g_uv = n_ab e^a_u e^b_v, where n_ab is the flat Minkowski metric. The 4 tetrad "
            "legs completely span the tangent space at each point.\n\n"
            "This is textbook differential geometry (Cartan; Misner-Thorne-Wheeler). The 4-leg "
            "structure is required to span a 4-dimensional tangent space. What the formalism "
            "demonstrates, without always stating explicitly, is that gravitational physics at "
            "each point has exactly 4 independent directions.\n\n"
            "Four legs. Four constraints. Four faces. The same structure appears wherever "
            "gravitational coupling is made explicit."
        )
    },
    {
        "id": "textbook_lqg",
        "title": "Loop Quantum Gravity: The Quantum Tetrahedron",
        "section": "Textbook Foundations",
        "order": 13,
        "content": (
            "Loop Quantum Gravity represents quantum states of geometry as spin networks: graphs "
            "with edges labeled by spins and nodes labeled by intertwiners. The result, "
            "established by Rovelli, Vidotto, and others, is that each 4-valent node corresponds "
            "to a quantum tetrahedron.\n\n"
            "This is theorem, not interpretation. The 4 edges meeting at a node represent the 4 "
            "faces of a tetrahedron. The intertwiner encodes how these faces fit together. The "
            "closure constraint requires that area-weighted normals sum to zero: sum(A_f n_f) = 0.\n\n"
            "This is textbook quantum gravity (Rovelli & Vidotto 2014). The tetrahedron emerges "
            "from the mathematics of quantized geometry as the minimal quantum of 3-dimensional "
            "space. It is not assumed; it is derived.\n\n"
            "The closure constraint in LQG is the quantum version of the ADM constraints. Both "
            "require k=4 directions. Both enforce geometric consistency. The classical "
            "tetrahedron and the quantum tetrahedron are the same geometry seen at different "
            "scales."
        )
    },
    {
        "id": "textbook_regge",
        "title": "Regge Calculus: The Discrete Simplex",
        "section": "Textbook Foundations",
        "order": 14,
        "content": (
            "Tullio Regge demonstrated in 1961 that general relativity can be formulated on "
            "simplicial complexes without coordinates. Spacetime is approximated by flat "
            "simplices glued together, with curvature concentrated at the hinges where "
            "simplices meet.\n\n"
            "In three spatial dimensions, the building block is the tetrahedron (4 vertices). "
            "In four-dimensional spacetime, the building block is the 4-simplex (5 vertices), "
            "bounded by 5 tetrahedra. The Regge action sums the deficit angles at each hinge. "
            "Smooth spacetime is recovered in the limit of many small simplices.\n\n"
            "This is textbook computational gravity (Regge 1961; Misner-Thorne-Wheeler Ch.42). "
            "Regge calculus demonstrates that the tetrahedron is the natural building block for "
            "discrete 3D geometry.\n\n"
            "ADM gives 4 constraints. Tetrad gives 4 legs. LQG gives 4 faces. Regge gives 4 "
            "vertices. Four independent formalisms, developed for different purposes, all "
            "arrive at the same geometric structure. This is either a remarkable coincidence "
            "or evidence that the structure is fundamental."
        )
    },
    
    # =========================================================================
    # SECTION VI: THE DUAL STRUCTURE
    # =========================================================================
    {
        "id": "one_tetrahedron",
        "title": "One Tetrahedron: Necessary but Insufficient",
        "section": "The Dual Structure",
        "order": 15,
        "content": (
            "A single tetrahedron provides the k=4 closure required to bound a region in 3D. It "
            "has 4 faces (coupling interfaces), 4 vertices (coupling channels), and 6 edges "
            "(connection pathways). This is the minimum structure for field closure.\n\n"
            "However, one tetrahedron is necessary but insufficient for complete gravitational "
            "physics. General relativity requires boundary conditions: the field equations "
            "determine dynamics, but initial and boundary data must be specified. In the ADM "
            "formalism, this appears as the distinction between the dynamical metric (evolved "
            "by the equations) and the reference structure (against which evolution is measured).\n\n"
            "A single tetrahedron represents only one metric. To represent both the dynamical "
            "geometry and the reference structure, a second tetrahedron is required. The "
            "question is how two tetrahedra must relate.\n\n"
            "The answer, as bimetric gravity demonstrates, is that they must share a center."
        )
    },
    {
        "id": "two_tetrahedra",
        "title": "Two Tetrahedra: The Stellated Octahedron",
        "section": "The Dual Structure",
        "order": 16,
        "content": (
            "Two interpenetrating tetrahedra with vertices at opposite corners of a cube form "
            "the stellated octahedron. This compound solid has 8 vertices (2k), 8 faces (2k), "
            "12 edges, and a central point where the two tetrahedra meet.\n\n"
            "Tetrahedron A has vertices at odd-parity positions: (0,0,1), (0,1,0), (1,0,0), "
            "(1,1,1). Tetrahedron B has vertices at even-parity positions: (0,0,0), (0,1,1), "
            "(1,0,1), (1,1,0). These positions are bitwise complements, creating perfect "
            "interlocking geometry with the tetrahedra sharing a common center.\n\n"
            "The stellated octahedron is not arbitrary. It is the unique compound that provides "
            "both k=4 closures (one per tetrahedron) while maintaining central symmetry. The "
            "central point, equidistant from all 8 vertices, is where the two tetrahedra meet "
            "on equal terms.\n\n"
            "This geometry has been known for centuries. Kepler studied it. What has not been "
            "widely recognized is its appearance at the heart of gravitational physics."
        )
    },
    {
        "id": "bimetric_requirement",
        "title": "The Bimetric Requirement",
        "section": "The Dual Structure",
        "order": 17,
        "content": (
            "The necessity of two tetrahedra becomes explicit in bimetric gravity. Hassan and "
            "Rosen (2012) demonstrated that consistent gravitational coupling requires two "
            "metrics to interact through a specific potential. The interaction must occur at "
            "a symmetric point where both metrics have equal standing, avoiding the ghost "
            "instabilities that arise from asymmetric treatment.\n\n"
            "The stellated octahedron provides this structure. Tetrahedron A corresponds to the "
            "physical metric g_uv. Tetrahedron B corresponds to the reference metric f_uv. The "
            "Field Origin at the center is equidistant from all vertices of both tetrahedra. "
            "The interaction potential evaluated at this point treats both metrics symmetrically, "
            "satisfying the symmetric vielbein condition required for ghost-free coupling.\n\n"
            "This is the geometric interpretation of textbook bimetric gravity. The mathematical "
            "requirements (symmetric vielbein, ghost-free interaction, equal treatment of both "
            "metrics) are satisfied by the stellated octahedron geometry.\n\n"
            "The structure was always there. The mathematics required it. The interpretation "
            "was missing."
        )
    },
    {
        "id": "why_dual_structure",
        "title": "The Logical Chain: Why Two Tetrahedra",
        "section": "The Dual Structure",
        "order": 18,
        "content": (
            "The argument for two tetrahedra follows a logical chain, each step grounded in "
            "textbook physics:\n\n"
            "Step 1: Enclosing 3D volume requires k=4 interfaces (simplex theorem, classical "
            "geometry).\n\n"
            "Step 2: The k=4 constraint appears in ADM, tetrad, LQG, Regge, and LIGO observations "
            "(textbook physics, observationally confirmed).\n\n"
            "Step 3: A single tetrahedron provides k=4 closure but represents only one metric "
            "(necessary but insufficient).\n\n"
            "Step 4: Complete gravitational physics requires both a dynamical metric and a "
            "reference structure (general relativity requires boundary conditions).\n\n"
            "Step 5: Two tetrahedra must share a common center for symmetric coupling (bimetric "
            "ghost-freedom requires symmetric vielbein condition, Hassan & Rosen 2012).\n\n"
            "Step 6: Interpenetrating tetrahedra at cube-opposite vertices form the stellated "
            "octahedron (unique geometry satisfying Steps 1-5).\n\n"
            "The dual structure is forced by the requirements. It is not chosen for aesthetics "
            "or convenience. It is the only geometry that satisfies the constraints."
        )
    },
    {
        "id": "face_structure",
        "title": "The 8-Face Structure: Time and Space",
        "section": "The Dual Structure",
        "order": 19,
        "content": (
            "The stellated octahedron has 8 faces: 4 from Tetrahedron A and 4 from Tetrahedron "
            "B. These faces divide into two categories based on their orientation relative to "
            "the central Field Origin.\n\n"
            "TIME faces (2 total): One face from each tetrahedron points toward the Field "
            "Origin. These are the inward-facing faces, corresponding to the timelike direction "
            "in the ADM decomposition. There is exactly 1 TIME face per tetrahedron, matching "
            "the 1 Hamiltonian constraint per metric.\n\n"
            "SPATIAL faces (6 total): Three faces from each tetrahedron point outward from the "
            "Field Origin. These are the outward-facing faces, corresponding to the three "
            "spatial directions. There are 3 SPATIAL faces per tetrahedron, matching the 3 "
            "momentum constraints per metric.\n\n"
            "This 1+3 structure (1 TIME, 3 SPATIAL per tetrahedron) is the geometric "
            "representation of the 3+1 decomposition. The 2 TIME faces and 6 SPATIAL faces "
            "encode the full constraint structure of bimetric gravity.\n\n"
            "The ADM decomposition, viewed geometrically, is a stellated octahedron."
        )
    },
    
    # =========================================================================
    # SECTION VII: THE FIELD DYNAMICS
    # =========================================================================
    {
        "id": "gravity_cells",
        "title": "Gravity Fields: The Cellular Structure of Space",
        "section": "Field Dynamics Introduction",
        "order": 20,
        "content": (
            "The human body contains approximately 37 trillion cells. Each cell is a complete "
            "functional unit with its own membrane, metabolism, and machinery. The 37 trillion "
            "cells work together seamlessly, producing the continuous appearance of a unified "
            "organism from the coordinated behavior of discrete units.\n\n"
            "Space follows the same pattern. The gravitational field consists of discrete units, "
            "each a stellated octahedron with its own geometry, closure, and coupling interfaces. "
            "These gravity fields work together seamlessly, producing the continuous appearance "
            "of spacetime from the coordinated behavior of discrete structures.\n\n"
            "The k=4 topology determines how gravity fields couple. Each field connects to "
            "neighbors through its 8 faces (4 per tetrahedron). Gravity fields exchange geometric "
            "information through shared boundaries. Closure constraints maintain consistent "
            "geometry across the lattice.\n\n"
            "The continuous spacetime of general relativity emerges from this discrete substrate, "
            "just as the continuous appearance of water emerges from discrete molecules."
        )
    },
    {
        "id": "k4_packing",
        "title": "k=4 Topology: Packing and Propagation",
        "section": "Field Dynamics Introduction",
        "order": 21,
        "content": (
            "The k=4 topology determines the packing geometry of gravity fields. Each field has "
            "8 coupling interfaces (4 faces per tetrahedron in the stellated octahedron). When "
            "fields pack together, these interfaces press against neighbor interfaces, creating "
            "a space-filling lattice.\n\n"
            "The simplex theorem guarantees that k=4 is the minimum for enclosing 3D volume. "
            "The dual structure doubles this to 2k=8 faces while maintaining the k=4 closure "
            "for each metric. The packing is efficient because it is minimal.\n\n"
            "This packing enables wave propagation. Adjacent gravity fields share interfaces and "
            "must achieve geometric consistency at boundaries. The closure constraint ensures "
            "this consistency. When one field is disturbed, it affects its neighbors, which "
            "affect their neighbors, propagating the disturbance through the lattice.\n\n"
            "Gravitational waves propagate through this structure. The medium is not mechanical "
            "but topological: disturbances in the coupling geometry of discrete field units."
        )
    },
    {
        "id": "emergent_physics",
        "title": "Emergent Physics from Geometry",
        "section": "Field Dynamics Introduction",
        "order": 22,
        "content": (
            "The stellated octahedron structure predicts specific physical values that would "
            "otherwise require separate postulates.\n\n"
            "Spin-1/2: The stellated octahedron has 8 faces total, of which 2 are TIME faces. "
            "The ratio (2/8) times total angular momentum (2h) equals h/2. Spin-1/2 follows "
            "from the face count.\n\n"
            "Charge quantization: Each tetrahedral face has 3 vertices corresponding to d=3 "
            "dimensions. Charge comes in units of 1/d = 1/3. The quark charges (+2/3, -1/3) "
            "correspond to vertex activation patterns on the two tetrahedra.\n\n"
            "MOND scale: The k=4 coupling structure has a saturation limit determined by the "
            "coupling geometry. When gravitational acceleration drops below a_0, the coupling "
            "channels operate differently. The MOND acceleration scale emerges from the "
            "geometry rather than being fitted to observations.\n\n"
            "These are not free parameters. They are consequences of the structure."
        )
    },
    {
        "id": "dark_matter_alternative",
        "title": "The Dark Matter Question",
        "section": "Field Dynamics Introduction",
        "order": 23,
        "content": (
            "When galactic rotation curves showed more gravity than visible matter could explain, "
            "two responses were possible. One was to add invisible matter. The other was to "
            "examine whether the gravitational field itself had structure that could account "
            "for the discrepancy.\n\n"
            "The first response became dark matter. The second was largely unexplored, despite "
            "the dual tetrahedral structure sitting in the textbook mathematics. The k=4 "
            "coupling topology, present in ADM, tetrad, LQG, and Regge formalisms, has "
            "consequences for how gravity behaves at low accelerations. These consequences "
            "were not calculated because the structure was not taken seriously as physics.\n\n"
            "The Gravity Field Dynamics model takes the structure seriously. The MOND "
            "phenomenology (flat rotation curves, the Tully-Fisher relation, the acceleration "
            "scale a_0) emerges from the coupling geometry of the stellated octahedron. The "
            "constitutive law mu(x) = x/(1+x) is derived from closure constraints, not fitted "
            "to data.\n\n"
            "Whether this accounts for all dark matter phenomenology remains to be tested. "
            "But the structure that might explain it was always there, waiting to be examined."
        )
    },
    {
        "id": "what_follows",
        "title": "From Foundation to Mechanism",
        "section": "Field Dynamics Introduction",
        "order": 24,
        "content": (
            "With the foundation established, the concepts and definitions that follow describe "
            "how the gravity field structure operates. The field dynamics explain:\n\n"
            "Field closure operates through the READ-SETTLE-REGISTER process, achieving "
            "consistency at boundaries while respecting causality.\n\n"
            "The Field Origin serves as both the coupling point and the gateway for nuclear "
            "binding, explaining atomic structure.\n\n"
            "The bidirectional compression shift releases energy during binding, explaining "
            "nuclear binding energy.\n\n"
            "The vortex pattern in the Field Chamber creates the electron, explaining "
            "electromagnetism as emergent from gravitational field dynamics.\n\n"
            "Uniform spin (chirality) enables spatial translation, explaining atomic motion "
            "through coupling and decoupling with empty gravity fields.\n\n"
            "Stellar compression forces gravity fields through Field Origins, explaining the "
            "stellar forge that builds the periodic table.\n\n"
            "The structure was always in the textbooks. What follows is the mechanics."
        )
    },
]


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_foundation(foundation_id):
    """Get a foundation entry by its ID."""
    for f in GFD_FOUNDATIONS:
        if f["id"] == foundation_id:
            return f
    return None


def get_foundations_by_section(section):
    """Get all foundations in a section."""
    return sorted(
        [f for f in GFD_FOUNDATIONS if f["section"] == section],
        key=lambda x: x["order"]
    )


def get_all_sections():
    """Get list of all sections in order."""
    sections = []
    for f in sorted(GFD_FOUNDATIONS, key=lambda x: x["order"]):
        if f["section"] not in sections:
            sections.append(f["section"])
    return sections


def get_foundations_in_order():
    """Get all foundations in display order."""
    return sorted(GFD_FOUNDATIONS, key=lambda x: x["order"])


# =============================================================================
# CHAIN OF LOGIC SUMMARY
# =============================================================================

CHAIN_SUMMARY = """
THE CHAIN OF LOGIC: WHY GRAVITY HAS THIS STRUCTURE

PROLOGUE
  1. The structure hiding in plain sight (40 years in the textbooks)

STARTING POINT
  2. Gravity is a field (confirmed physics)
  3. Question: one field or many?

PROBLEMS WITH ONE FIELD
  4. Thermodynamic problem (no local processing mechanism)
  5. Information problem (nothing to carry gravitational waves)
  6. Constraint problem (cannot satisfy ADM constraints locally)

RESOLUTION: MANY FIELDS
  7. Discrete field units resolve all three problems
  8. Simplex theorem: k=4 interfaces required (geometric necessity)

OBSERVATIONAL CONFIRMATION
  9. LIGO confirms k=4 (measured 2 polarizations = 10 - 2k)
  10. Wave propagation through discrete medium

TEXTBOOK FOUNDATIONS
  11. ADM: 4 constraints (1 Hamiltonian + 3 momentum)
  12. Tetrad: 4 basis vectors (the name means four)
  13. LQG: 4 faces of quantum tetrahedron
  14. Regge: 4 vertices of 3-simplex

THE DUAL STRUCTURE
  15. One tetrahedron: necessary but insufficient
  16. Two tetrahedra form stellated octahedron
  17. Bimetric gravity requires symmetric coupling
  18. Logical chain: why two tetrahedra are forced
  19. 8-face structure: 2 TIME + 6 SPATIAL

FIELD DYNAMICS
  20. Gravity fields: cellular structure of space
  21. k=4 packing enables wave propagation
  22. Emergent physics: spin-1/2, charge quantization, MOND scale
  23. The dark matter question
  24. Foundation complete; mechanics follow
"""


def print_chain_summary():
    """Print the chain of logic summary."""
    print(CHAIN_SUMMARY)


def print_foundation_reference():
    """Print a quick reference of the chain of logic."""
    sections = get_all_sections()
    for section in sections:
        print(f"\n{'='*70}")
        print(f"  {section.upper()}")
        print(f"{'='*70}")
        for f in get_foundations_by_section(section):
            print(f"\n  {f['order']}. {f['title']}")
            print(f"  {'-'*60}")
            # Print first paragraph
            first_para = f['content'].split('\n\n')[0]
            words = first_para.split()
            line = "  "
            for word in words[:30]:  # First ~30 words
                if len(line) + len(word) + 1 <= 72:
                    line += word + " "
                else:
                    print(line.rstrip())
                    line = "  " + word + " "
            if line.strip():
                print(line.rstrip() + "...")


if __name__ == "__main__":
    print("Gravity Field Dynamics: Foundations")
    print("=" * 50)
    print(f"Total entries: {len(GFD_FOUNDATIONS)}")
    print(f"Sections: {len(get_all_sections())}")
    print_chain_summary()
