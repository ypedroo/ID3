import math


class ID3:
    def read_data(self, filename):
        find = open(filename, "r")
        data = []
        d = []
        for line in find.readlines():
            d.append(line.strip())
        for d1 in d:
            data.append(d1.split(","))
        find.close()

        self.featureNames = self.get_features(data)
        data = data[1:]
        self.classes = self.get_classes(data)
        data = self.get_pure_data(data)

        return data, self.classes, self.featureNames

    def get_classes(self, data):
        # data = data[1:]
        classes = []
        for d in range(len(data)):
            classes.append(data[d][-1])
        return classes

    def get_features(self, data):
        features = data[0]
        features = features[:-1]
        return features

    def get_pure_data(self, dataRows):
        # dataRows = dataRows[1:]
        for d in range(len(dataRows)):
            dataRows[d] = dataRows[d][:-1]
        return dataRows

    def empty_list(self, size):
        values = []
        for i in range(size):
            values.append(0)
        return values

    def get_max(self, atr):
        atr_max = max(atr)
        idx = atr.index(atr_max)
        return idx

    def get_distinct_values(self, dataList):
        distinctValues = []
        for item in dataList:
            if (distinctValues.count(item) == 0):
                distinctValues.append(item)
        return distinctValues

    def get_distinct_values_table(self, dataTable, column):
        distinctValues = []
        for row in dataTable:
            if (distinctValues.count(row[column]) == 0):
                distinctValues.append(row[column])
        return distinctValues

    def get_entropy(self, prop):
        if (prop != 0):
            return -prop * math.log2(prop)
        else:
            return 0

    def create_tree(self, trainingData, classes, features, maxlevel=-1, level=0):
        newData = len(trainingData)
        newFeature = len(features)

        newClasses = self.get_distinct_values(classes)
        frequency = self.empty_list(len(newClasses))
        totalEntropy = 0
        index = 0

        for aclass in newClasses:
            frequency[index] = classes.count(aclass)
            prob = float(frequency[index]) / newData
            totalEntropy += self.get_entropy(prob)
            index += 1
        default = classes[self.get_max(frequency)]
        if (newData == 0 or newFeature == 0 or (maxlevel >= 0 and level > maxlevel)):
            return default
        elif classes.count(classes[0]) == newData:  # Testa se todos as classes sao iguais
            return classes[0]
        else:
            gain = self.empty_list(newFeature)
            for feature in range(newFeature):
                g = self.get_gain(trainingData, classes, feature)
                gain[feature] = totalEntropy - g

            bestFeature = self.get_max(gain)
            newTree = {features[bestFeature]: {}}

            values = self.get_distinct_values_table(trainingData, bestFeature)
            for value in values:
                newData = []
                newClasses = []
                index = 0
                for row in trainingData:
                    if row[bestFeature] == value:
                        if bestFeature == 0:
                            newRow = row[1:]
                            newNames = features[1:]
                        elif bestFeature == newFeature:
                            newRow = row[:-1]
                            newNames = features[:-1]
                        else:
                            newRow = row[:bestFeature]
                            newRow.extend(row[bestFeature + 1:])
                            newNames = features[:bestFeature]
                            newNames.extend(features[bestFeature + 1:])
                        newData.append(newRow)
                        newClasses.append(classes[index])
                    index += 1

                subtree = self.create_tree(newData, newClasses, newNames, maxlevel, level + 1)

                newTree[features[bestFeature]][value] = subtree
            return newTree

    def get_gain(self, data, classes, feature):
        gain = 0
        newData = len(data)

        values = self.get_distinct_values_table(data, feature)  # valores distintos da coluna
        featureCounts = self.empty_list(len(values))
        entropy = self.empty_list(len(values))
        valueIndex = 0
        for value in values:
            dataIndex = 0
            newClasses = []
            for row in data:
                if row[feature] == value:
                    featureCounts[valueIndex] += 1  # quantidade de cada feature distinta
                    newClasses.append(classes[dataIndex])  # pega as classes de cada feature
                dataIndex += 1

            classValues = self.get_distinct_values(newClasses)
            classCounts = self.empty_list(len(classValues))
            classIndex = 0
            for classValue in classValues:
                for aclass in newClasses:
                    if aclass == classValue:
                        classCounts[classIndex] += 1
                classIndex += 1

            for classIndex in range(len(classValues)):
                currentClass = float(classCounts[classIndex]) / sum(classCounts)  #
                entropy[valueIndex] += self.get_entropy(currentClass)

            pn = float(featureCounts[valueIndex]) / newData
            gain = gain + pn * entropy[valueIndex]

            valueIndex += 1
        return gain

    def printTree(self, dic, seperator):
        if type(dic) == dict:
            for item in dic.items():
                print(seperator, item[0])
                self.printTree(item[1], seperator + " | ")
        else:
            print(seperator + " -> (", dic + ")")


tree = ID3()
tree_data, leaf_node, dec_node = tree.read_data('loan.dat')

ntree = tree.create_tree(tree_data, leaf_node, dec_node)

tree.printTree(ntree, ' ')
