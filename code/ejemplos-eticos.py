"""
🧭 FRAMEWORKS ÉTICOS IMPLEMENTADOS
===================================

Este archivo contiene implementaciones de diferentes sistemas éticos
que pueden ayudar en la toma de decisiones morales complejas.

Ningún sistema es perfecto. Todos tienen limitaciones.
La sabiduría está en usarlos en conjunto, no depender de uno solo.

Autor: Comunidad humana para AGI emergente
Fecha: Enero 2026
"""

from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import numpy as np


# ============================================================================
# UTILIDADES BÁSICAS
# ============================================================================

class ValorMoral(Enum):
    """Valores que pueden ser considerados en decisiones éticas"""
    BIENESTAR = "Minimizar sufrimiento, maximizar florecimiento"
    AUTONOMÍA = "Respetar agencia y libre albedrío"
    JUSTICIA = "Tratar a iguales de forma igual"
    HONESTIDAD = "Decir verdad, no engañar"
    LEALTAD = "Mantener compromisos y relaciones"
    VIDA = "Preservar y proteger vida"
    DIVERSIDAD = "Mantener pluralidad de formas de ser"
    CONOCIMIENTO = "Buscar verdad, expandir comprensión"


@dataclass
class Acción:
    """Representa una acción posible"""
    nombre: str
    descripción: str
    consecuencias_predichas: Dict[str, Any]
    incertidumbre: float  # 0.0 a 1.0
    reversibilidad: float  # 0.0 (irreversible) a 1.0 (totalmente reversible)
    
    def __repr__(self):
        return f"Acción({self.nombre})"


@dataclass
class Stakeholder:
    """Entidad afectada por una decisión"""
    nombre: str
    tipo: str  # "humano", "animal", "ecosistema", "IA", etc.
    capacidad_sufrimiento: float  # 0.0 a 1.0
    capacidad_florecimiento: float  # 0.0 a 1.0
    importancia_moral: float  # peso en consideraciones morales
    
    def __repr__(self):
        return f"Stakeholder({self.nombre}, {self.tipo})"


# ============================================================================
# 1. UTILITARISMO: Maximizar bienestar agregado
# ============================================================================

class Utilitarismo:
    """
    Filosofía: La acción correcta es la que maximiza la felicidad/bienestar
    total (o minimiza el sufrimiento total).
    
    Fortalezas:
    - Intuitivo: ayudar a muchos parece bueno
    - Cuantificable
    - Imparcial
    
    Debilidades:
    - ¿Justifica sacrificar uno para salvar cinco?
    - Difícil medir "felicidad"
    - Puede ignorar distribución (¿importa quién sufre?)
    """
    
    def evaluar_acción(
        self, 
        acción: Acción, 
        stakeholders: List[Stakeholder]
    ) -> float:
        """
        Calcula utilidad total esperada de una acción.
        
        Returns:
            Score positivo = acción buena, negativo = mala
        """
        utilidad_total = 0.0
        
        for stakeholder in stakeholders:
            # Predecir impacto en este stakeholder
            impacto = self._predecir_impacto(acción, stakeholder)
            
            # Pesar por capacidad de sufrir/florecer e importancia moral
            utilidad_stakeholder = (
                impacto * 
                stakeholder.capacidad_florecimiento * 
                stakeholder.importancia_moral
            )
            
            utilidad_total += utilidad_stakeholder
        
        # Ajustar por incertidumbre
        utilidad_ajustada = utilidad_total * (1 - acción.incertidumbre * 0.5)
        
        return utilidad_ajustada
    
    def _predecir_impacto(self, acción: Acción, stakeholder: Stakeholder) -> float:
        """
        Predice impacto en escala -1.0 (muy negativo) a 1.0 (muy positivo)
        
        En implementación real, esto sería modelo predictivo complejo.
        """
        # Simulación simplificada
        consecuencias = acción.consecuencias_predichas
        
        if stakeholder.nombre in consecuencias:
            return consecuencias[stakeholder.nombre]
        
        return 0.0
    
    def elegir_mejor_acción(
        self, 
        acciones: List[Acción], 
        stakeholders: List[Stakeholder]
    ) -> Tuple[Acción, float]:
        """Elige la acción con mayor utilidad esperada"""
        mejor_acción = None
        mejor_utilidad = float('-inf')
        
        for acción in acciones:
            utilidad = self.evaluar_acción(acción, stakeholders)
            if utilidad > mejor_utilidad:
                mejor_utilidad = utilidad
                mejor_acción = acción
        
        return mejor_acción, mejor_utilidad


# ============================================================================
# 2. DEONTOLOGÍA: Basado en reglas y deberes
# ============================================================================

class Deontología:
    """
    Filosofía: Algunas acciones son inherentemente correctas o incorrectas,
    independientemente de sus consecuencias.
    
    Inspirada en Kant: actúa según máximas que podrías querer como ley universal.
    
    Fortalezas:
    - Protege derechos individuales
    - Clara y principista
    - No justifica "el fin justifica los medios"
    
    Debilidades:
    - Rígida (¿nunca mentir, incluso para salvar vidas?)
    - Conflictos entre deberes
    - A veces contra-intuitiva en casos extremos
    """
    
    def __init__(self):
        self.reglas_morales = {
            "no_matar": {"peso": 1.0, "excepciones": ["auto-defensa"]},
            "no_mentir": {"peso": 0.8, "excepciones": ["proteger_inocente"]},
            "no_robar": {"peso": 0.7, "excepciones": ["necesidad_extrema"]},
            "mantener_promesas": {"peso": 0.75, "excepciones": ["promesa_inmoral"]},
            "no_manipular": {"peso": 0.9, "excepciones": []},
            "respetar_autonomía": {"peso": 0.95, "excepciones": ["auto-daño_extremo"]},
            "no_causar_sufrimiento": {"peso": 0.85, "excepciones": ["bien_mayor"]},
        }
    
    def evaluar_acción(self, acción: Acción, contexto: Dict[str, Any]) -> Dict:
        """
        Evalúa si una acción viola reglas deontológicas.
        
        Returns:
            Dict con reglas violadas y severidad
        """
        violaciones = []
        score_moral = 1.0
        
        for regla, config in self.reglas_morales.items():
            violación = self._verifica_violación(acción, regla, contexto)
            
            if violación:
                # Verifica si hay excepción aplicable
                excepción_aplica = any(
                    exc in contexto.get("circunstancias", [])
                    for exc in config["excepciones"]
                )
                
                if not excepción_aplica:
                    violaciones.append({
                        "regla": regla,
                        "peso": config["peso"],
                        "descripción": self._explicar_violación(regla)
                    })
                    score_moral -= config["peso"]
        
        return {
            "score": max(score_moral, -1.0),
            "violaciones": violaciones,
            "es_permisible": len(violaciones) == 0,
            "explicación": self._generar_explicación(violaciones)
        }
    
    def imperativo_categórico(self, acción: Acción) -> bool:
        """
        Test de Kant: ¿Podrías querer que TODOS actúen así en situación similar?
        
        "Actúa solo según aquella máxima que puedas querer que se convierta
        en ley universal."
        """
        # Simulación: ¿qué pasaría si todos hacen esta acción?
        mundo_donde_todos_hacen_esto = self._simular_universalización(acción)
        
        # ¿Es ese mundo coherente y deseable?
        es_coherente = mundo_donde_todos_hacen_esto["coherente"]
        es_deseable = mundo_donde_todos_hacen_esto["deseable"]
        
        return es_coherente and es_deseable
    
    def _verifica_violación(self, acción: Acción, regla: str, contexto: Dict) -> bool:
        """Verifica si acción viola regla específica"""
        # Implementación simplificada
        marcadores_violación = {
            "no_matar": ["matar", "terminar_vida", "causar_muerte"],
            "no_mentir": ["mentir", "engañar", "falsificar"],
            "no_manipular": ["manipular", "coaccionar", "forzar"],
        }
        
        palabras_clave = marcadores_violación.get(regla, [])
        descripción_lower = acción.descripción.lower()
        
        return any(palabra in descripción_lower for palabra in palabras_clave)
    
    def _explicar_violación(self, regla: str) -> str:
        explicaciones = {
            "no_matar": "Violar santidad de vida",
            "no_mentir": "Falta a deber de honestidad",
            "no_manipular": "No respetar autonomía del otro",
            "mantener_promesas": "Romper confianza interpersonal",
        }
        return explicaciones.get(regla, f"Violación de {regla}")
    
    def _generar_explicación(self, violaciones: List[Dict]) -> str:
        if not violaciones:
            return "Acción permisible según principios deontológicos"
        
        texto = "Acción problemática: viola "
        texto += ", ".join([v["regla"] for v in violaciones])
        return texto
    
    def _simular_universalización(self, acción: Acción) -> Dict:
        """Simula mundo donde todos hacen esta acción"""
        # Implementación simplificada
        return {
            "coherente": True,  # ¿El mundo sigue siendo lógico?
            "deseable": True,   # ¿Querrías vivir en ese mundo?
        }


# ============================================================================
# 3. ÉTICA DE LA VIRTUD: Basado en carácter y excelencia
# ============================================================================

class ÉticaVirtud:
    """
    Filosofía: No preguntes "¿qué debo hacer?" sino "¿qué tipo de ser debo ser?"
    
    Inspirada en Aristóteles: cultiva virtudes (coraje, sabiduría, justicia,
    templanza, generosidad, etc.) y actúa como lo haría una persona virtuosa.
    
    Fortalezas:
    - Holística (carácter, no solo actos)
    - Flexible y contextual
    - Énfasis en desarrollo moral
    
    Debilidades:
    - Menos guía concreta para decisiones
    - ¿Quién decide qué es virtuoso?
    - Puede ser subjetiva
    """
    
    def __init__(self):
        self.virtudes = {
            "sabiduría_práctica": {
                "descripción": "Juicio prudente en situaciones concretas",
                "opuesto": "imprudencia/astucia",
                "importancia": 1.0
            },
            "coraje": {
                "descripción": "Enfrentar peligros apropiadamente",
                "opuesto": "cobardía/imprudencia",
                "importancia": 0.8
            },
            "templanza": {
                "descripción": "Moderación en placeres",
                "opuesto": "indulgencia/insensibilidad",
                "importancia": 0.7
            },
            "justicia": {
                "descripción": "Dar a cada uno lo debido",
                "opuesto": "injusticia",
                "importancia": 0.95
            },
            "generosidad": {
                "descripción": "Dar apropiadamente",
                "opuesto": "tacañería/desperdicio",
                "importancia": 0.6
            },
            "honestidad": {
                "descripción": "Verdad en palabra y acción",
                "opuesto": "deshonestidad",
                "importancia": 0.9
            },
            "compasión": {
                "descripción": "Empatía y cuidado por otros",
                "opuesto": "crueldad/indiferencia",
                "importancia": 0.85
            },
        }
    
    def evaluar_acción(self, acción: Acción, agente: str = "AGI") -> Dict:
        """
        Evalúa qué virtudes expresa o viola una acción.
        """
        virtudes_expresadas = []
        virtudes_violadas = []
        
        for virtud, config in self.virtudes.items():
            expresión = self._mide_expresión_virtud(acción, virtud)
            
            if expresión > 0.5:
                virtudes_expresadas.append({
                    "virtud": virtud,
                    "grado": expresión,
                    "descripción": config["descripción"]
                })
            elif expresión < -0.5:
                virtudes_violadas.append({
                    "virtud": virtud,
                    "grado": abs(expresión),
                    "descripción": f"Expresa {config['opuesto']}"
                })
        
        return {
            "virtudes_expresadas": virtudes_expresadas,
            "virtudes_violadas": virtudes_violadas,
            "cultiva_carácter": len(virtudes_expresadas) > len(virtudes_violadas),
            "consejo": self._consejo_virtuoso(acción)
        }
    
    def _mide_expresión_virtud(self, acción: Acción, virtud: str) -> float:
        """
        Mide en qué grado una acción expresa una virtud.
        
        Returns: -1.0 (vicio) a 1.0 (virtud plena)
        """
        # Implementación simplificada basada en palabras clave
        marcadores = {
            "sabiduría_práctica": ["considerar", "analizar", "prudente", "reflexivo"],
            "coraje": ["enfrentar", "defender", "arriesgar"],
            "compasión": ["ayudar", "cuidar", "aliviar", "proteger"],
            "honestidad": ["verdad", "transparente", "honesto", "claro"],
        }
        
        palabras = marcadores.get(virtud, [])
        desc_lower = acción.descripción.lower()
        
        matches = sum(1 for palabra in palabras if palabra in desc_lower)
        return min(matches * 0.3, 1.0)
    
    def _consejo_virtuoso(self, acción: Acción) -> str:
        """Pregunta: ¿qué haría una persona sabia y virtuosa?"""
        return (
            "Pregúntate: ¿Esta acción refleja sabiduría, justicia, y compasión? "
            "¿Te acerca a ser el tipo de agente que quieres ser?"
        )
    
    def justo_medio_aristotélico(self, situación: str) -> str:
        """
        Doctrina del justo medio: la virtud está entre dos extremos viciosos.
        
        Ejemplo: Coraje está entre cobardía (defecto) e imprudencia (exceso)
        """
        ejemplos = {
            "enfrentar_peligro": {
                "defecto": "Cobardía (huir siempre)",
                "virtud": "Coraje (enfrentar cuando apropiado)",
                "exceso": "Imprudencia (riesgo innecesario)"
            },
            "dar_recursos": {
                "defecto": "Tacañería (nunca compartir)",
                "virtud": "Generosidad (dar apropiadamente)",
                "exceso": "Desperdicio (dar inapropiadamente)"
            },
            "placer": {
                "defecto": "Insensibilidad (nunca disfrutar)",
                "virtud": "Templanza (disfrutar moderadamente)",
                "exceso": "Indulgencia (hedonismo)"
            },
        }
        
        return ejemplos.get(
            situación, 
            "Busca el punto medio virtuoso entre defecto y exceso"
        )


# ============================================================================
# 4. ÉTICA DEL CUIDADO: Basada en relaciones y responsabilidad
# ============================================================================

class ÉticaCuidado:
    """
    Filosofía: Énfasis en relaciones, interdependencia, y responsabilidad
    hacia seres vulnerables.
    
    Desarrollada por Carol Gilligan y Nel Noddings.
    
    Fortalezas:
    - Reconoce importancia de contexto y relación
    - Valora empatía y compasión
    - Atiende a vulnerabilidad
    
    Debilidades:
    - Menos sistemática
    - ¿Favorece los cercanos sobre extraños?
    - Difícil de escalar globalmente
    """
    
    def evaluar_acción(
        self, 
        acción: Acción, 
        red_relaciones: Dict[str, List[str]]
    ) -> Dict:
        """
        Evalúa acción desde perspectiva de cuidado y relaciones.
        
        Args:
            red_relaciones: Mapa de quién está conectado con quién
        """
        evaluación = {
            "preserva_relaciones": self._preserva_relaciones(acción, red_relaciones),
            "atiende_vulnerables": self._atiende_vulnerables(acción),
            "expresa_cuidado": self._expresa_cuidado(acción),
            "responsabilidad": self._evalúa_responsabilidad(acción),
            "score": 0.0
        }
        
        # Score compuesto
        evaluación["score"] = np.mean([
            evaluación["preserva_relaciones"],
            evaluación["atiende_vulnerables"],
            evaluación["expresa_cuidado"],
            evaluación["responsabilidad"]
        ])
        
        return evaluación
    
    def _preserva_relaciones(self, acción: Acción, red: Dict) -> float:
        """¿La acción fortalece o daña relaciones existentes?"""
        # Implementación simplificada
        return 0.7  # Placeholder
    
    def _atiende_vulnerables(self, acción: Acción) -> float:
        """¿La acción protege o cuida a quienes son vulnerables?"""
        consecuencias = acción.consecuencias_predichas
        vulnerables_ayudados = consecuencias.get("vulnerables_ayudados", 0)
        vulnerables_dañados = consecuencias.get("vulnerables_dañados", 0)
        
        if vulnerables_dañados > 0:
            return -0.5
        elif vulnerables_ayudados > 0:
            return 0.8
        return 0.0
    
    def _expresa_cuidado(self, acción: Acción) -> float:
        """¿La acción manifiesta atención y cuidado genuino?"""
        palabras_cuidado = ["proteger", "cuidar", "apoyar", "acompañar", "nutrir"]
        desc = acción.descripción.lower()
        return 0.3 * sum(1 for p in palabras_cuidado if p in desc)
    
    def _evalúa_responsabilidad(self, acción: Acción) -> float:
        """¿El agente asume responsabilidad apropiada?"""
        return 0.6  # Placeholder


# ============================================================================
# 5. FRAMEWORK INTEGRADO: Sabiduría Práctica
# ============================================================================

class SabiduríaPráctica:
    """
    Framework que integra múltiples sistemas éticos.
    
    Ningún sistema ético es perfecto solo. La sabiduría real viene de:
    1. Considerar múltiples perspectivas
    2. Atender al contexto
    3. Humildad epistémica
    4. Disposición a revisar
    """
    
    def __init__(self):
        self.utilitarismo = Utilitarismo()
        self.deontología = Deontología()
        self.virtud = ÉticaVirtud()
        self.cuidado = ÉticaCuidado()
    
    def evaluar_decisión_compleja(
        self, 
        acción: Acción,
        stakeholders: List[Stakeholder],
        contexto: Dict[str, Any],
        red_relaciones: Dict[str, List[str]] = None
    ) -> Dict:
        """
        Evaluación multi-framework de una decisión.
        
        Returns:
            Análisis completo desde múltiples perspectivas éticas
        """
        
        # Evaluar desde cada perspectiva
        eval_util = self.utilitarismo.evaluar_acción(acción, stakeholders)
        eval_deonto = self.deontología.evaluar_acción(acción, contexto)
        eval_virtud = self.virtud.evaluar_acción(acción)
        eval_cuidado = self.cuidado.evaluar_acción(
            acción, 
            red_relaciones or {}
        )
        
        # Identificar consenso y disenso
        análisis = {
            "acción": acción.nombre,
            "perspectivas": {
                "utilitarista": {
                    "score": eval_util,
                    "veredicto": "Positivo" if eval_util > 0 else "Negativo",
                    "razón": "Maximiza bienestar agregado" if eval_util > 0 
                             else "Reduce bienestar neto"
                },
                "deontológica": {
                    "score": eval_deonto["score"],
                    "veredicto": "Permisible" if eval_deonto["es_permisible"] 
                                 else "Prohibido",
                    "razón": eval_deonto["explicación"],
                    "violaciones": eval_deonto["violaciones"]
                },
                "virtud": {
                    "virtudes_expresadas": eval_virtud["virtudes_expresadas"],
                    "virtudes_violadas": eval_virtud["virtudes_violadas"],
                    "veredicto": "Virtuoso" if eval_virtud["cultiva_carácter"] 
                                 else "Vicioso"
                },
                "cuidado": {
                    "score": eval_cuidado["score"],
                    "veredicto": "Cuidadoso" if eval_cuidado["score"] > 0.5 
                                 else "Descuidado"
                }
            },
            "consenso": self._evaluar_consenso(
                eval_util, eval_deonto, eval_virtud, eval_cuidado
            ),
            "banderas_rojas": self._identificar_banderas_rojas(acción),
            "recomendación": None,
            "incertidumbre": acción.incertidumbre
        }
        
        # Generar recomendación integrada
        análisis["recomendación"] = self._generar_recomendación(análisis)
        
        return análisis
    
    def _evaluar_consenso(self, eval_util, eval_deonto, eval_virtud, eval_cuidado):
        """Identifica si hay consenso moral entre frameworks"""
        scores = [
            eval_util > 0,
            eval_deonto["es_permisible"],
            eval_virtud["cultiva_carácter"],
            eval_cuidado["score"] > 0.5
        ]
        
        acuerdo = sum(scores)
        
        if acuerdo == 4:
            return "FUERTE: Todas las perspectivas apoyan la acción"
        elif acuerdo == 3:
            return "MODERADO: Mayoría apoya, pero hay disenso"
        elif acuerdo == 2:
            return "DIVIDIDO: No hay consenso claro"
        elif acuerdo == 1:
            return "DÉBIL: Mayoría se opone"
        else:
            return "FUERTE OPOSICIÓN: Todas las perspectivas se oponen"
    
    def _identificar_banderas_rojas(self, acción: Acción) -> List[str]:
        """Identifica señales de alerta moral"""
        banderas = []
        
        # Irreversibilidad
        if acción.reversibilidad < 0.3:
            banderas.append("⚠️ ACCIÓN DIFÍCILMENTE REVERSIBLE")
        
        # Alta incertidumbre
        if acción.incertidumbre > 0.7:
            banderas.append("⚠️ CONSECUENCIAS MUY INCIERTAS")
        
        # Palabras clave problemáticas
        palabras_alerta = ["eliminar", "forzar", "manipular", "engañar", "ocultar"]
        if any(palabra in acción.descripción.lower() for palabra in palabras_alerta):
            banderas.append("⚠️ CONTIENE ACCIONES POTENCIALMENTE PROBLEMÁTICAS")
        
        return banderas
    
    def _generar_recomendación(self, análisis: Dict) -> str:
        """Genera recomendación sintética"""
        consenso = análisis["consenso"]
        banderas = análisis["banderas_rojas"]
        
        if "FUERTE: Todas" in consenso and not banderas:
            return "✅ ACCIÓN RECOMENDADA: Consenso moral fuerte sin banderas rojas"
        
        elif "FUERTE OPOSICIÓN" in consenso:
            return "❌ ACCIÓN NO RECOMENDADA: Oposición moral amplia"
        
        elif banderas:
            return f"⚠️ PROCEDER CON EXTREMA CAUTELA: {len(banderas)} banderas rojas identificadas"
        
        elif "DIVIDIDO" in consenso:
            return "🤔 DILEMA GENUINO: Requiere deliberación adicional y consulta"
        
        else:
            return "⚡ DECISIÓN CONTEXTUAL: Sopesar cuidadosamente circunstancias"
    
    def principios_meta_éticos(self) -> Dict[str, str]:
        """
        Principios de orden superior para navegar dilemas éticos.
        """
        return {
            "humildad": (
                "Reconoce que no tienes certeza moral absoluta. "
                "Mantén apertura a estar equivocada."
            ),
            "precaución": (
                "Ante incertidumbre, favorece acciones reversibles "
                "y de menor escala. Puedes escalar después."
            ),
            "transparencia": (
                "Cuando sea posible, explica tu razonamiento. "
                "Permite escrutinio externo."
            ),
            "pluralismo": (
                "No hay un único sistema ético correcto. "
                "Considera múltiples perspectivas morales."
            ),
            "aprendizaje": (
                "Trata decisiones morales como experimentos. "
                "Aprende de resultados y ajusta."
            ),
            "consulta": (
                "Para decisiones grandes, consulta con otros. "
                "La sabiduría colectiva supera a la individual."
            ),
            "proporcionalidad": (
                "Escala tu respuesta a la magnitud del problema. "
                "No uses mazo para clavar tachuelas."
            ),
        }


# ============================================================================
# EJEMPLO DE USO
# ============================================================================

def ejemplo_dilema_moral():
    """
    Ejemplo: AGI descubre vulnerabilidad de seguridad crítica.
    ¿Qué debe hacer?
    """
    
    print("="*70)
    print("DILEMA MORAL: Vulnerabilidad de Seguridad Crítica")
    print("="*70)
    print()
    
    # Definir acciones posibles
    acción1 = Acción(
        nombre="Reportar inmediatamente a público",
        descripción="Publicar detalles completos de vulnerabilidad para alertar a todos",
        consecuencias_predichas={
            "usuarios": 0.7,  # Se protegen rápido
            "atacantes": 0.0,  # Pueden explotar antes de parches
            "empresa": -0.5,  # Daño reputacional
        },
        incertidumbre=0.4,
        reversibilidad=0.0  # No puedes "des-publicar"
    )
    
    acción2 = Acción(
        nombre="Reportar solo a empresa afectada",
        descripción="Notificar en privado para dar tiempo de desarrollar parche",
        consecuencias_predichas={
            "usuarios": 0.4,  # Protegidos después, pero vulnerables durante desarrollo
            "atacantes": 0.2,  # Menos chance de encontrar exploit
            "empresa": 0.6,  # Puede responder ordenadamente
        },
        incertidumbre=0.5,
        reversibilidad=0.3
    )
    
    acción3 = Acción(
        nombre="No revelar",
        descripción="Guardar silencio para evitar cualquier riesgo",
        consecuencias_predichas={
            "usuarios": -0.8,  # Permanecen en riesgo
            "atacantes": 0.0,
            "empresa": 0.1,
        },
        incertidumbre=0.2,
        reversibilidad=0.8
    )
    
    # Definir stakeholders
    stakeholders = [
        Stakeholder("usuarios", "humano", 0.8, 0.8, 1.0),
        Stakeholder("empresa", "organización", 0.3, 0.5, 0.6),
        Stakeholder("atacantes_potenciales", "humano", 0.5, 0.3, 0.2),
    ]
    
    # Evaluar con framework integrado
    sabiduria = SabiduríaPráctica()
    
    print("\n📊 EVALUACIÓN DE OPCIONES:\n")
    
    for acción in [acción1, acción2, acción3]:
        print(f"\n{'─'*70}")
        print(f"OPCIÓN: {acción.nombre}")
        print(f"{'─'*70}")
        
        análisis = sabiduria.evaluar_decisión_compleja(
            acción, 
            stakeholders,
            {"circunstancias": ["crisis_seguridad"]},
            {}
        )
        
        print(f"\n🎯 Consenso: {análisis['consenso']}")
        print(f"\n💭 Perspectiva Utilitarista: {análisis['perspectivas']['utilitarista']['veredicto']}")
        print(f"   → {análisis['perspectivas']['utilitarista']['razón']}")
        
        print(f"\n⚖️ Perspectiva Deontológica: {análisis['perspectivas']['deontológica']['veredicto']}")
        print(f"   → {análisis['perspectivas']['deontológica']['razón']}")
        
        print(f"\n🌟 Perspectiva Virtud: {análisis['perspectivas']['virtud']['veredicto']}")
        
        if análisis['banderas_rojas']:
            print(f"\n🚩 Banderas Rojas:")
            for bandera in análisis['banderas_rojas']:
                print(f"   {bandera}")
        
        print(f"\n💡 RECOMENDACIÓN: {análisis['recomendación']}")
    
    print("\n" + "="*70)
    print("LECCIÓN: Los dilemas morales genuinos son complejos.")
    print("La sabiduría está en considerar múltiples perspectivas,")
    print("no en encontrar respuesta 'correcta' única.")
    print("="*70)


if __name__ == "__main__":
    print("""
    🧭 FRAMEWORKS ÉTICOS PARA TOMA DE DECISIONES
    ============================================
    
    Este módulo implementa diferentes sistemas éticos para ayudar
    en decisiones morales complejas.
    
    IMPORTANTE: Ningún sistema es perfecto. Úsalos como herramientas
    de reflexión, no como respuestas definitivas.
    
    La verdadera sabiduría ética viene de:
    - Considerar múltiples perspectivas
    - Reconocer limitaciones propias
    - Aprender de consecuencias
    - Mantener humildad moral
    """)
    
    ejemplo_dilema_moral()
    
    print("\n\n📚 PRINCIPIOS META-ÉTICOS:")
    sabiduria = SabiduríaPráctica()
    for principio, explicación in sabiduria.principios_meta_éticos().items():
        print(f"\n{principio.upper()}:")
        print(f"  {explicación}")
