# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\PiratePlay\views\selected_movie.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SelectedMovie(object):
    def setupUi(self, SelectedMovie):
        SelectedMovie.setObjectName("SelectedMovie")
        SelectedMovie.resize(1090, 839)
        self.verticalLayout = QtWidgets.QVBoxLayout(SelectedMovie)
        self.verticalLayout.setObjectName("verticalLayout")
        self.resultsScrollArea = QtWidgets.QScrollArea(SelectedMovie)
        self.resultsScrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.resultsScrollArea.setWidgetResizable(True)
        self.resultsScrollArea.setObjectName("resultsScrollArea")
        self.resultsArea = QtWidgets.QWidget()
        self.resultsArea.setGeometry(QtCore.QRect(0, 0, 1072, 821))
        self.resultsArea.setObjectName("resultsArea")
        self.resultsLayout = QtWidgets.QVBoxLayout(self.resultsArea)
        self.resultsLayout.setSpacing(15)
        self.resultsLayout.setObjectName("resultsLayout")
        self.detailsTabWidget = QtWidgets.QTabWidget(self.resultsArea)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.detailsTabWidget.sizePolicy().hasHeightForWidth())
        self.detailsTabWidget.setSizePolicy(sizePolicy)
        self.detailsTabWidget.setMinimumSize(QtCore.QSize(0, 500))
        self.detailsTabWidget.setObjectName("detailsTabWidget")
        self.infoTab = QtWidgets.QWidget()
        self.infoTab.setObjectName("infoTab")
        self.infoLayout = QtWidgets.QVBoxLayout(self.infoTab)
        self.infoLayout.setObjectName("infoLayout")
        self.infoContentLayout = QtWidgets.QHBoxLayout()
        self.infoContentLayout.setObjectName("infoContentLayout")
        self.posterLayout = QtWidgets.QVBoxLayout()
        self.posterLayout.setSpacing(5)
        self.posterLayout.setObjectName("posterLayout")
        self.posterLabel = QtWidgets.QLabel(self.infoTab)
        self.posterLabel.setMinimumSize(QtCore.QSize(300, 400))
        self.posterLabel.setMaximumSize(QtCore.QSize(16777215, 500))
        self.posterLabel.setText("")
        self.posterLabel.setObjectName("posterLabel")
        self.posterLayout.addWidget(self.posterLabel)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.posterLayout.addItem(spacerItem)
        self.infoContentLayout.addLayout(self.posterLayout)
        self.infoGroupBox = QtWidgets.QGroupBox(self.infoTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.infoGroupBox.sizePolicy().hasHeightForWidth())
        self.infoGroupBox.setSizePolicy(sizePolicy)
        self.infoGroupBox.setMinimumSize(QtCore.QSize(0, 400))
        self.infoGroupBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.infoGroupBox.setTitle("")
        self.infoGroupBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.infoGroupBox.setObjectName("infoGroupBox")
        self.infoGridLayout = QtWidgets.QGridLayout(self.infoGroupBox)
        self.infoGridLayout.setContentsMargins(0, -1, -1, -1)
        self.infoGridLayout.setObjectName("infoGridLayout")
        self.movieDetailsLayout = QtWidgets.QGridLayout()
        self.movieDetailsLayout.setObjectName("movieDetailsLayout")
        self.tomatometerLabel = QtWidgets.QLabel(self.infoGroupBox)
        self.tomatometerLabel.setText("")
        self.tomatometerLabel.setObjectName("tomatometerLabel")
        self.movieDetailsLayout.addWidget(self.tomatometerLabel, 3, 0, 1, 1)
        self.releaseYearLabel = QtWidgets.QLabel(self.infoGroupBox)
        self.releaseYearLabel.setText("")
        self.releaseYearLabel.setObjectName("releaseYearLabel")
        self.movieDetailsLayout.addWidget(self.releaseYearLabel, 0, 0, 1, 1)
        self.userScoreValue = QtWidgets.QLabel(self.infoGroupBox)
        self.userScoreValue.setText("")
        self.userScoreValue.setObjectName("userScoreValue")
        self.movieDetailsLayout.addWidget(self.userScoreValue, 2, 1, 1, 1)
        self.ytLabel = QtWidgets.QLabel(self.infoGroupBox)
        self.ytLabel.setText("")
        self.ytLabel.setObjectName("ytLabel")
        self.movieDetailsLayout.addWidget(self.ytLabel, 5, 0, 1, 1)
        self.popcornmeterLabel = QtWidgets.QLabel(self.infoGroupBox)
        self.popcornmeterLabel.setText("")
        self.popcornmeterLabel.setObjectName("popcornmeterLabel")
        self.movieDetailsLayout.addWidget(self.popcornmeterLabel, 4, 0, 1, 1)
        self.popcornmeterValue = QtWidgets.QLabel(self.infoGroupBox)
        self.popcornmeterValue.setText("")
        self.popcornmeterValue.setObjectName("popcornmeterValue")
        self.movieDetailsLayout.addWidget(self.popcornmeterValue, 4, 1, 1, 1)
        self.tomatometerValue = QtWidgets.QLabel(self.infoGroupBox)
        self.tomatometerValue.setText("")
        self.tomatometerValue.setObjectName("tomatometerValue")
        self.movieDetailsLayout.addWidget(self.tomatometerValue, 3, 1, 1, 1)
        self.userScoreLabel = QtWidgets.QLabel(self.infoGroupBox)
        self.userScoreLabel.setText("")
        self.userScoreLabel.setObjectName("userScoreLabel")
        self.movieDetailsLayout.addWidget(self.userScoreLabel, 2, 0, 1, 1)
        self.metascoreLabel = QtWidgets.QLabel(self.infoGroupBox)
        self.metascoreLabel.setText("")
        self.metascoreLabel.setObjectName("metascoreLabel")
        self.movieDetailsLayout.addWidget(self.metascoreLabel, 1, 0, 1, 1)
        self.releaseYearValue = QtWidgets.QLabel(self.infoGroupBox)
        self.releaseYearValue.setText("")
        self.releaseYearValue.setObjectName("releaseYearValue")
        self.movieDetailsLayout.addWidget(self.releaseYearValue, 0, 1, 1, 1)
        self.metascoreValue = QtWidgets.QLabel(self.infoGroupBox)
        self.metascoreValue.setText("")
        self.metascoreValue.setObjectName("metascoreValue")
        self.movieDetailsLayout.addWidget(self.metascoreValue, 1, 1, 1, 1)
        self.ytValue = QtWidgets.QLabel(self.infoGroupBox)
        self.ytValue.setText("")
        self.ytValue.setObjectName("ytValue")
        self.movieDetailsLayout.addWidget(self.ytValue, 5, 1, 1, 1)
        self.infoGridLayout.addLayout(self.movieDetailsLayout, 5, 0, 1, 1)
        self.imdbRatingLabel = QtWidgets.QLabel(self.infoGroupBox)
        self.imdbRatingLabel.setText("")
        self.imdbRatingLabel.setObjectName("imdbRatingLabel")
        self.infoGridLayout.addWidget(self.imdbRatingLabel, 3, 0, 1, 1)
        self.genresLabel = QtWidgets.QLabel(self.infoGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.genresLabel.sizePolicy().hasHeightForWidth())
        self.genresLabel.setSizePolicy(sizePolicy)
        self.genresLabel.setText("")
        self.genresLabel.setObjectName("genresLabel")
        self.infoGridLayout.addWidget(self.genresLabel, 2, 0, 1, 1)
        self.movieTitleLabel = QtWidgets.QLabel(self.infoGroupBox)
        self.movieTitleLabel.setText("")
        self.movieTitleLabel.setObjectName("movieTitleLabel")
        self.infoGridLayout.addWidget(self.movieTitleLabel, 0, 0, 1, 1)
        self.plotLabel = QtWidgets.QLabel(self.infoGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plotLabel.sizePolicy().hasHeightForWidth())
        self.plotLabel.setSizePolicy(sizePolicy)
        self.plotLabel.setText("")
        self.plotLabel.setWordWrap(True)
        self.plotLabel.setObjectName("plotLabel")
        self.infoGridLayout.addWidget(self.plotLabel, 8, 0, 1, 1)
        self.infoContentLayout.addWidget(self.infoGroupBox)
        self.infoLayout.addLayout(self.infoContentLayout)
        self.detailsTabWidget.addTab(self.infoTab, "")
        self.detailsTab = QtWidgets.QWidget()
        self.detailsTab.setObjectName("detailsTab")
        self.detailsLayout = QtWidgets.QVBoxLayout(self.detailsTab)
        self.detailsLayout.setObjectName("detailsLayout")
        self.detailsTextBrowser = QtWidgets.QTextBrowser(self.detailsTab)
        self.detailsTextBrowser.setObjectName("detailsTextBrowser")
        self.detailsLayout.addWidget(self.detailsTextBrowser)
        self.detailsTabWidget.addTab(self.detailsTab, "")
        self.downloadTab = QtWidgets.QWidget()
        self.downloadTab.setObjectName("downloadTab")
        self.downloadLayout = QtWidgets.QVBoxLayout(self.downloadTab)
        self.downloadLayout.setObjectName("downloadLayout")
        self.downloadsGridLayout = QtWidgets.QGridLayout()
        self.downloadsGridLayout.setObjectName("downloadsGridLayout")
        self.downloadLayout.addLayout(self.downloadsGridLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.downloadLayout.addItem(spacerItem1)
        self.detailsTabWidget.addTab(self.downloadTab, "")
        self.resultsLayout.addWidget(self.detailsTabWidget)
        self.errorLabel = QtWidgets.QLabel(self.resultsArea)
        self.errorLabel.setVisible(False)
        self.errorLabel.setObjectName("errorLabel")
        self.resultsLayout.addWidget(self.errorLabel)
        self.noResultsLabel = QtWidgets.QLabel(self.resultsArea)
        self.noResultsLabel.setVisible(False)
        self.noResultsLabel.setObjectName("noResultsLabel")
        self.resultsLayout.addWidget(self.noResultsLabel)
        self.successLabel = QtWidgets.QLabel(self.resultsArea)
        self.successLabel.setVisible(False)
        self.successLabel.setObjectName("successLabel")
        self.resultsLayout.addWidget(self.successLabel)
        self.resultsScrollArea.setWidget(self.resultsArea)
        self.verticalLayout.addWidget(self.resultsScrollArea)

        self.retranslateUi(SelectedMovie)
        self.detailsTabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(SelectedMovie)

    def retranslateUi(self, SelectedMovie):
        _translate = QtCore.QCoreApplication.translate
        SelectedMovie.setWindowTitle(_translate("SelectedMovie", "Selected Movie"))
        self.detailsTabWidget.setTabText(self.detailsTabWidget.indexOf(self.infoTab), _translate("SelectedMovie", "Info"))
        self.detailsTabWidget.setTabText(self.detailsTabWidget.indexOf(self.detailsTab), _translate("SelectedMovie", "Details"))
        self.detailsTabWidget.setTabText(self.detailsTabWidget.indexOf(self.downloadTab), _translate("SelectedMovie", "Download"))
        self.noResultsLabel.setText(_translate("SelectedMovie", "No results found"))