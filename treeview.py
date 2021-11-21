# -*- codage : utf-8 -*-

##################################################### ############################
#
# Droit d'auteur (C) 2012-2014
# Xavier Izard
#
# Ce fichier fait partie de DXF2GCODE.
#
# DXF2GCODE est un logiciel libre : vous pouvez le redistribuer et/ou modifier
# sous les termes de la licence publique générale GNU telle que publiée par
# la Free Software Foundation, soit la version 3 de la Licence, soit
# (à votre choix) toute version ultérieure.
#
# DXF2GCODE est distribué dans l'espoir qu'il sera utile,
# mais SANS AUCUNE GARANTIE ;  sans même la garantie implicite de
# COMMERCIALISATION ou ADÉQUATION À UN USAGE PARTICULIER.  Voir le
# Licence publique générale GNU pour plus de détails.
#
# Vous devriez avoir reçu une copie de la licence publique générale GNU
# avec DXF2GCODE.  Sinon, consultez <http://www.gnu.org/licenses/>.
#
##################################################### ############################

"""
La classe TreeView est une sous-classe de la classe QT QTreeView.
La sous-classe est effectuée afin de :
- mettre en place un simple (c'est-à-dire pas complexe) drag & drop
- obtenir des événements de sélection
@newfield objectif : objectif
@newfield sideeffect : Effet secondaire, Effets secondaires

@purpose : afficher l'arborescence du fichier .dxf, sélectionner,
          activer et définir l'ordre d'exportation des formes
"""
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QTreeView


class TreeView(QTreeView):
    """
    Sous-classé QTreeView pour répondre à nos besoins.
    Implémenter un simple (c'est-à-dire pas complexe) glisser-déposer, obtenir des événements de sélection
    """

    def __init__(self, parent=None):
        """
        Initialisation de la classe TreeView.
        """
        QTreeView.__init__(self, parent)

        self.dragged_element = False  # Aucun élément n'est actuellement glissé et déposé
        self.dragged_element_model_index = None
        self.selectionChangedcallback = None
        self.keyPressEventcallback = None
        self.signals_blocked = False  # Transmettre les événements entre les classes

        self.pressed.connect(self.elementPressed)

    def setExportOrderUpdateCallback(self, callback):
        self.exportOrderUpdateCallback = callback

    def setSelectionCallback(self, callback):
        """
        Enregistrer une fonction de rappel appelée lorsque la sélection change
        sur les options TreeView
        @param callback : fonction avec prototype functionName(parent, sélectionné, désélectionné) :
        """
        self.selectionChangedcallback = callback

    def setKeyPressEventCallback(self, callback):
        """
        Enregistrer une fonction de rappel appelée lorsqu'une touche est enfoncée sur le TreeView
        @param callback : fonction avec prototype : accepté functionName(key_code, item_index):
        """
        self.keyPressEventcallback = callback

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            # Capture mouse press so that selection doesn't change
            # on right click
            pass
        else:
            QTreeView.mousePressEvent(self, event)

    def dragEnterEvent(self, event):
        """
        Définissez flag dragged_element sur True (nous avons commencé un glisser).
        Remarque : nous ne pouvons pas obtenir l'index glissé à partir de cette fonction car
        il est appelé très tard dans la chaîne de traînée.  Si l'utilisateur est trop
        rapide en glisser-déposer, alors event.pos() retournera une position
        qui est sensiblement différente de la position d'origine lorsque l'utilisateur
        commencé à faire glisser l'élément.  Nous ne stockons donc qu'un drapeau.  Nous avons déjà
        fait glisser l'élément via la fonction elementPressed().
        options
        @param event : le dragEvent (contient la position, ...)
        print("\033[32;1mdragEnterEvent {0} at pos({1}), index = {2}\033[m\n".format(event, event.pos(), self.indexAt(event.pos ()).parent().internalId()))
        """
        self.dragged_element = True
        event.acceptProposedAction()

    def elementPressed(self, element_model_index):
        """
        Cette fonction est appelée lorsqu'un élément (Forme, ...) est appuyé
        avec la souris.  Il vise à stocker l'index (QModelIndex) de
        l'élément enfoncé.
        options
        @param element_model_index : QModelIndex de l'élément pressé
        print("\033[32melementPressed row = {0}\033[m".format(element_model_index.model().itemFromIndex(element_model_index).row()))
        """
        # enregistrer l'index de l'élément cliqué...
        self.dragged_element_model_index = element_model_index

    # def dropEvent(self, event):
    #     """
    #     Cette fonction est appelée lorsque l'utilisateur a relâché la souris
    #     pour déposer un élément à l'emplacement du pointeur de la souris.
    #     Remarque : nous avons totalement réimplémenté cette fonction car le
    #     l'implémentation par défaut de QT veut copier et supprimer chaque traîné
    #     élément, même lorsque nous n'utilisons que les internes se déplacent à l'intérieur du treeView.
    #     C'est totalement inutile et trop compliqué pour nous car
    #     cela impliquerait d'implémenter une importation et une exportation QMimeData
    #     fonctions pour exporter nos Formes / Calques / Entités.  Le code
    #     ci-dessous essaie de déplacer les éléments au bon endroit lorsqu'ils sont
    #     chuté ;  il utilise des permutations de listes simples (c'est-à-dire pas de doublons
    #     & supprime).
    #     options
    #     @param event : le dropEvent (contient la position, ...)
    #     print("\033[32mdropEvent {0} at pos({1}).{3}, index = {2}\033[m\n".format(event, event.pos(), self.indexAt(event .pos()).parent().internalId(), self.dropIndicatorPosition()))
    #     """
    #     drag_item=None
    #     if   self.dragged_element and  self.dragged_element_model_index:
    #     # print("action proposée = {0}".format(event.proposedAction()))
    #         event.setDropAction(QtCore.Qt.IgnoreAction)
    #         event.accept()
    #
    #         drag_item = self.dragged_element_model_index.model().itemFromIndex(self.dragged_element_model_index)
    #         items_parent = drag_item.parent()
    #     else:
    #         #items_parent:
    #     # parent vaut 0, nous devons donc obtenir l'élément racine de l'arbre en tant que parent...
    #         items_parent = drag_item.model().invisibleRootItem()
    #
    #
    #     drop_model_index = self.indexAt(event.pos())
    #     # Obtenir la position d'insertion liée à l'élément déposé :
    #     # OnItem, AboveItem, BelowItem, OnViewport...
    #     position_relative = self.dropIndicatorPosition()
    #
    #     # calculer la nouvelle position du calque ou de la forme
    #     if drop_model_index.isValid() and relative_position != QTreeView.OnViewport:
    #     # drop position est calculable à partir d'un élément réel
    #         drop_item = drop_model_index.model().itemFromIndex(drop_model_index)
    #
    #     if drag_item.parent() == drop_item.parent():
    #
    #         drag_row = self.dragged_element_model_index.row()  # ligne d'origine
    #     # ligne de destination (+1 si la position relative est inférieure à l'élément drop)...
    #         drop_row = drop_model_index.row() + (1 si relative_position == QTreeView.BelowItem sinon 0)
    #     # print("\033[32;1mACCEPTÉ!\033[m\n")
    #
    #     elif (drag_item.parent() == drop_item ou non drop_item.parent() \
    #         and
    #     drag_item.parent() == drop_item.model().invisibleRootItem().child(drop_item.row(), 0)) \
    #         and(relative_position == QTreeView.BelowItem or relative_position == QTreeView.OnItem):
    #     # nous sommes sur l'élément parent (le deuxième test prend la première colonne
    #     # de la ligne de drop_item.  La première colonne est l'endroit où se trouvent les enfants
    #     # inséré, il faut donc comparer avec cette col)
    #
    #     # ligne d'origine...
    #         drag_row = self.dragged_element_model_index.row()
    #     # ligne de destination est 0 car l'élément est déposé sur le parent...
    #         drop_row = 0
    #     # print("\033[32;1mACCEPTÉ SUR PARENT!\033[m\n")
    #     elif (pas drop_item.parent() and self.dragged_element_model_index.parent().sibling(self.dragged_element_model_index.parent().row() + 1,
    #                                                       0) == drop_item.model().invisibleRootItem().child(drop_item.row(),
    #                                                                                                         0).index()) \
    #         et(relative_position == QTreeView.AboveItem
    #     or
    #     relative_position == QTreeView.OnItem):
    #     # nous sommes sur l'élément parent suivant => insérer à la fin du calque de l'élément déplacé
    #     # ligne d'origine...
    #     drag_row = self.dragged_element_model_index.row()
    #     # insérer à la fin...
    #     drop_row = items_parent.rowCount()
    #     # print("\033[32;1mACCEPTÉ SUR LE PROCHAIN ​​PARENT !\033[m\n")
    #
    #     autre:
    #     # nous sommes dans la mauvaise branche de l'arbre,
    #     Impossible
    #     de
    #     coller  # élément ici
    #     drop_row = -1
    #     # print("\033[31;1mREFUSÉ!\033[m\n")
    #
    #     autre:
    #     # Nous sommes en dessous de n'importe quel élément d'arbre => insérer à la fin
    #     drag_row = self.dragged_element_model_index.row()  # ligne d'origine
    #     drop_row = items_parent.rowCount()  # insérer à la fin
    #     # print("\033[32;1mACCEPTÉ À LA FIN!\033[m\n")
    #
    #     # déplacer efficacement l'élément
    #     si
    #     drop_row >= 0:
    #     # print("de la ligne {0} à la ligne {1}".format(drag_row, drop_row))
    #
    #     item_to_be_moved = items_parent.takeRow(drag_row)
    #     if  drop_row > drag_row:
    #         # nous avons un élément de moins dans la liste, donc si l'élément est
    #         # traîné en dessous de sa position d'origine, nous devons
    #         # corriger sa position d'insertion
    #         drop_row -= 1
    #         items_parent.insertRow(drop_row, item_to_be_moved)
    #
    #     elif  self.signals_blocked:
    #         # Signalez que l'ordre du TreeView a changé...
    #         self.exportOrderUpdateCallback()
    #         self.dragged_element = False
    #     else :
    #         event.ignore()
    #
    #
    # def moveUpCurrentItem(self):
    #     """
    #     Déplacer l'élément actuel vers le haut.  Ce slot a vocation à être connecté à un bouton.
    #     S'il n'y a pas d'élément en cours, ne faites rien.
    #     """
    #     current_item_index = self.currentIndex()
    #     si
    #     current_item_index
    #     et
    #     current_item_index.isValid():
    #     current_item = current_item_index.model().itemFromIndex(current_item_index)
    #     current_item_parent = current_item.parent()
    #     sinon
    #     current_item_parent:
    #     # parent vaut 0, nous devons donc obtenir l'élément racine de l'arbre en tant que parent...
    #     current_item_parent = current_item.model().invisibleRootItem()
    #
    #
    #     pop_row = current_item_index.row()  # ligne d'origine
    #     push_row = pop_row - 1
    #     si
    #     push_row >= 0:
    #     item_to_be_moved = current_item_parent.takeRow(pop_row)
    #     current_item_parent.insertRow(push_row, item_to_be_moved)
    #     self.setCurrentIndex(current_item.index())
    #
    #     sinon
    #     self.signals_blocked:
    #     # Signale que l'ordre du TreeView a changé
    #     self.exportOrderUpdateCallback()
    #
    #
    # def moveDownCurrentItem(self):
    #     """
    #     Déplacer l'élément actuel vers le bas.  Ce slot a vocation à être connecté à un bouton.
    #     S'il n'y a pas d'élément en cours, ne faites rien.
    #     """
    #     current_item_index = self.currentIndex()
    #     if current_item_index and  current_item_index.isValid():
    #         current_item = current_item_index.model().itemFromIndex(current_item_index)
    #         current_item_parent = current_item.parent()
    #     else:
    #         current_item_parent:
    #     # parent vaut 0, nous devons donc obtenir l'élément racine de l'arbre en tant que parent...
    #         current_item_parent = current_item.model().invisibleRootItem()
    #
    #
    #     pop_row = current_item_index.row()  # ligne d'origine
    #     push_row = pop_row + 1
    #     if  push_row < current_item_parent.rowCount():
    #         item_to_be_moved = current_item_parent.takeRow(pop_row)
    #         current_item_parent.insertRow(push_row, item_to_be_moved)
    #         self.setCurrentIndex(current_item.index())
    #
    #     else:
    #     self.signals_blocked:
    #     # Signalez que l'ordre du TreeView a changé...
    #     self.exportOrderUpdateCallback()

    def blockSignals(self, block):
        """
        Bloque les signaux de cette classe.  Sous-classé afin de bloquer également
        selectionModification des options de "signal" (rappel)
        @param block : s'il faut bloquer le signal (True) ou non (False)
        """
        self.signals_blocked = block
        QTreeView.blockSignals(self, block)

    def selectionChanged(self, selected, deselected):
        """
        Function called by QT when the selection has changed for this treeView.
        Subclassed in order to call a callback function options
        @param selected: list of selected items
        @param deselected: list of deselected items
        print("\033[32;1mselectionChanged selected count = {0} ; deselected count = {1}\033[m".format(selected.count(), deselected.count()))
        """
        QTreeView.selectionChanged(self, selected, deselected)

        if self.selectionChangedcallback and not self.signals_blocked:
            self.selectionChangedcallback(self, selected, deselected)

    def keyPressEvent(self, keyEvent):
        """
        Function called by QT when a key has been pressed inside the treeView.
        Subclassed in order to call a callback function
        @param keyEvent: keyboard event
        print("\033[31;1mkeyPressEvent() key = {0}\033[m".format(keyEvent.key()))    """

        if self.keyPressEventcallback and not self.signals_blocked:
            if not self.keyPressEventcallback(keyEvent):
                # key not accepted => send it back to the parent
                QTreeView.keyPressEvent(self, keyEvent)
        else:
            QTreeView.keyPressEvent(self, keyEvent)


class MyStandardItemModel(QStandardItemModel):
    """
    Sous-classe QStandardItemModel pour éviter les erreurs lors de l'utilisation du glisser-déposer
    """

    def __init__(self, parent=None):
        """
        Initialisation de la classe MyStandardItemModel.
        """
        QStandardItemModel.__init__(self, parent)

    def mimeData(self, index):
        """
        Cette fonction est appelée par QT à chaque fois qu'une opération glisser est
        initié, pour sérialiser les données associées au
        élément déplacé.  Cependant, QT ne sait pas comment sérialiser un Shape
        ou un Layer, donc ça renvoie une erreur... puisque nous gérons le Drag & Drop
        en interne, nous n'avons pas besoin de sérialisation, donc nous sous-classons
        la fonction et ne retourne rien (astuce pour éviter les erreurs).
        """
        mimeData = QtCore.QMimeData()
        # mimeData.setData("application/x-qabstractitemmodeldatalist", "")
        mimeData.setData("application/x-qstandarditemmodeldatalist", "")

        return mimeData
